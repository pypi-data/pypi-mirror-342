from PIL import Image
from torchvision import transforms
import math
import torch.nn.functional as F
from functools import reduce
import random
import torch
import torch.nn as nn
from huggingface_hub import hf_hub_download
import warnings

warnings.filterwarnings('ignore')


class Charm_Tokenizer(nn.Module):
    """
    Charm Tokenizer prioritizes high-resolution details in important regions while downscaling others.
    This module tokenizes images while preserving Composition, High-resolution details, Aspect Ratio,
    and Multi-scale information simultaneously.
    This is particularly useful for image aesthetic and quality assessment.

    Args:
        patch_selection (str): The method for selecting important patches
            (options: ['saliency', 'random', 'frequency', 'gradient', 'entropy', 'original']).
        training_dataset (str): Used to set the number of ViT input tokens to match a specific training dataset from the paper.(default: 'aadb').
        backbone (str): The ViT backbone model (default: 'facebook/dinov2-small').
        factor (float): The downscaling factor for less important patches (default: 0.5).
        scales (int): The number of scales used for multiscale processing (default: 2).
        random_crop_size (tuple): Used for the 'original' patch selection strategy (default: (224, 224)).
        downscale_shortest_edge (int): Used for the 'original' patch selection strategy (default: 256).
        without_pad_or_dropping (bool): Whether to avoid padding or dropping patches (default: True).
    """

    def __init__(self, patch_selection='frequency', training_dataset='aadb', backbone='facebook/dinov2-small', factor=0.5,
                 scales=2, random_crop_size=(224, 224), downscale_shortest_edge=256, without_pad_or_dropping=True):
        super().__init__()
        self.augmentation = 'all'
        self.without_pad_or_dropping = without_pad_or_dropping
        self.model = backbone
        if training_dataset == None:
            self.dataset = 'spaq'
        else:
            self.dataset = training_dataset
        self.patch_selection_strategy = patch_selection
        self.pos_embeds = {}
        self.prepare_config()
        self.load_pos_embed(backbone)
        self.interpolate_offset = 0.1
        self.num_scales = scales
        self.factor = factor
        self.scale_factor = [self.factor] + [s * ((1 - self.factor) / (self.num_scales - 1)) + self.factor for s in
                                             range(self.num_scales)[1:]]
        self.scaled_patchsizes = [int(element * ((2 ** (self.num_scales - 1)) * self.patch_size)) for element in
                                  self.scale_factor]
        self.initial_hidden_size = 512
        self.random_crop_size = random_crop_size
        self.downscale_shortest_edge = downscale_shortest_edge

    def load_pos_embed(self, model_name):
        if model_name == 'facebook/dinov2-small':
            path = hf_hub_download(repo_id="FatemehBehrad/Charm", filename='dino_small_pos.pt')
        elif model_name == 'facebook/dinov2-large':
            path = hf_hub_download(repo_id="FatemehBehrad/Charm", filename='dino_large.pt')
        else:
            ValueError(
                'The Library only support Dinov2-small :) Please refer to Github for other backbone.')
        self.pos_embed = torch.load(path).detach()

    def prepare_config(self):
        if self.dataset == 'ava':
            self.hidden_size = 512
        elif self.dataset == 'tad66k':
            self.hidden_size = 768
        else:
            self.hidden_size = 1024
        self.hidden_size = self.hidden_size + 1
        if 'dino' in self.model:
            self.patch_size = 14
            self.patch_stride = 14
        elif 'vit' in self.model:
            if 'small' in self.model:
                self.patch_size = 16
                self.patch_stride = 16
            elif 'base' in self.model:
                self.patch_size = 32
                self.patch_stride = 32
            else:
                ValueError(
                    'Model is not supported. Choose from: Dinov2-large / Dinov2-Base / Dinov2-large / ViT-small / ViT-base')

    def resize(self, img):
        height, width = img.shape[1:]
        shortest_edge = min(height, width)
        if shortest_edge == self.downscale_shortest_edge:
            return img
        elif shortest_edge < self.downscale_shortest_edge:
            diff_w = ((self.downscale_shortest_edge - width) // 2) + 1
            diff_h = ((self.downscale_shortest_edge - height) // 2) + 1
            if diff_h < 0:
                diff_h = 0
            if diff_w < 0:
                diff_w = 0
            transform = transforms.Pad((diff_w, diff_h))
            img = transform(img)
        else:
            if height > width:
                scale_factor = height / width
                new_width = self.downscale_shortest_edge
                new_height = self.downscale_shortest_edge * scale_factor
            else:
                scale_factor = width / height
                new_height = self.downscale_shortest_edge
                new_width = self.downscale_shortest_edge * scale_factor

            resize = transforms.Resize((int(new_height), int(new_width)), antialias=True)
            # Apply the transformation to your image tensor
            img = resize(img)
        return img

    def random_crop(self, img, mask=None):

        max_y_start = img.shape[1] - self.random_crop_size[0] + 1
        max_x_start = img.shape[2] - self.random_crop_size[1] + 1

        y_start = torch.randint(0, max_y_start, size=(1,))
        x_start = torch.randint(0, max_x_start, size=(1,))
        cropped_image = img[:, y_start:y_start + self.random_crop_size[0], x_start:x_start + self.random_crop_size[1]]

        if mask is not None:
            cropped_mask = mask[:, y_start:y_start + self.random_crop_size[0],
                           x_start:x_start + self.random_crop_size[1]]
        else:
            cropped_mask = None

        return cropped_image, cropped_mask

    def add_padding(self, img, patch_size):
        channels, height, width = img.size()

        if width % patch_size != 0:
            padding_width = (patch_size - (width % patch_size)) % patch_size
        else:
            padding_width = 0

        if height % patch_size != 0:
            padding_height = (patch_size - (height % patch_size)) % patch_size
        else:
            padding_height = 0

        padding = torch.nn.ZeroPad2d((0, padding_width, 0, padding_height))
        padded_img = padding(img)

        return padded_img

    def image_to_patches(self, image, patch_size, stride=None):
        channels, height, width = image.size()
        if stride is None:
            stride = patch_size

        patches = []
        for y in range(0, height - patch_size + 1, stride):
            for x in range(0, width - patch_size + 1, stride):
                patch = image[:, y:y + patch_size, x:x + patch_size]
                patches.append(patch)
            if width % patch_size != 0:
                # Add remaining parts along the right edge
                x = width - patch_size
                remaining_patch = image[:, y:y + patch_size, x:width]
                patches.append(remaining_patch)

        return patches

    def interpolate_positional_embedding(self, pos_embed, size, interpolate_offset, dim):
        w0, h0 = size
        w0, h0 = w0 + interpolate_offset, h0 + interpolate_offset
        N = pos_embed.shape[1] - 1
        pos_embed = pos_embed.float()
        class_pos_embed = pos_embed[:, 0]
        patch_pos_embed = pos_embed[:, 1:]
        sqrt_N = math.sqrt(N)
        sx, sy = float(w0) / sqrt_N, float(h0) / sqrt_N
        patch_pos_embed = nn.functional.interpolate(
            patch_pos_embed.reshape(1, int(sqrt_N), int(sqrt_N), dim).permute(0, 3, 1, 2),
            scale_factor=(sx, sy),
            mode="bicubic",
            align_corners=False,
        )
        assert int(w0) == patch_pos_embed.shape[-2]
        assert int(h0) == patch_pos_embed.shape[-1]
        patch_pos_embed = patch_pos_embed.permute(0, 2, 3, 1).view(1, -1, dim)
        return patch_pos_embed, class_pos_embed

    def padding(self, x, max_seq_len):
        n_crops, c, W, H = x.size()
        padding = torch.zeros(max_seq_len, c, W, H, dtype=x.dtype, device=x.device)
        x = torch.cat([x, padding], dim=0)
        x = x[:max_seq_len, :, :, :]
        return x

    def cropping(self, image, target_size):
        channels, height, width = image.shape
        crop_width = width % target_size
        crop_height = height % target_size

        end_x = width - crop_width
        end_y = height - crop_height

        cropped_image = image[:, :end_y, :end_x]

        return cropped_image

    def pad_or_crop(self, image, size):
        channels, height, width = image.shape

        crop_width = width % size
        crop_height = height % size
        if crop_height == 0:
            crop_height = 1
        if crop_width == 0:
            crop_width = 1
        total_pixel_crop = crop_height * crop_width

        if width % size != 0:
            padding_width = (size - (width % size)) % size
        else:
            padding_width = 1
        if height % size != 0:
            padding_height = (size - (height % size)) % size
        else:
            padding_height = 1
        total_pixel_pad = padding_height * padding_width

        if total_pixel_pad > total_pixel_crop:
            new_image = self.cropping(image, size)
        else:
            new_image = self.add_padding(image, size)

        return new_image

    def lcm(self, arr):
        l = reduce(lambda x, y: (x * y) // math.gcd(x, y), arr)
        return l

    def patch_selection_frequency_based(self, frequencies, n_patches, scale, num_scales):
        if scale == num_scales - 1:
            bluriness, indices = zip(*frequencies[-1 * n_patches:])
        else:
            bluriness, indices = zip(*frequencies[-4 * n_patches:-2 * n_patches])
        selected_indices = random.sample(indices, n_patches)  # To add stochasticity
        return selected_indices

    def patch_selection_entropy_based(self, entropies, n_patches, scale, num_scales):
        if scale == num_scales - 1:
            bluriness, indices = zip(*entropies[-1 * n_patches:])
        else:
            bluriness, indices = zip(*entropies[-4 * n_patches:-2 * n_patches])
        selected_indices = random.sample(indices, n_patches)  # To add stochasticity
        return selected_indices

    def patch_selection_gradient(self, gradients, n_patches, scale, num_scales):
        if scale == num_scales - 1:
            grads, indices = zip(*gradients[-1 * n_patches:])
        else:
            grads, indices = zip(*gradients[-4 * n_patches:-2 * n_patches])
        selected_indices = random.sample(indices, n_patches)  # To add stochasticity
        return selected_indices

    def patch_selection_saliency(self, salient_indices, n_patches):
        selected_indices = random.sample(salient_indices, n_patches)
        return selected_indices

    def patch_selection(self, patch_selection, importance, n_patches, scale, total_patches):
        if patch_selection == 'random':
            selected_indices = random.sample(total_patches, n_patches)
        elif patch_selection == 'frequency':
            selected_indices = self.patch_selection_frequency_based(importance, n_patches, scale, self.num_scales)
        elif patch_selection == 'entropy':
            selected_indices = self.patch_selection_entropy_based(importance, n_patches, scale, self.num_scales)
        elif patch_selection == 'gradient':
            selected_indices = self.patch_selection_gradient(importance, n_patches, scale, self.num_scales)
        elif patch_selection == 'saliency':
            if len(importance) >= n_patches:
                selected_indices = self.patch_selection_saliency(importance, n_patches)
            else:
                if set(total_patches).isdisjoint(set(importance)):
                    selected_indices = random.sample(total_patches, n_patches)
                else:
                    non_salient = list(set(total_patches) - set(importance))
                    extra = n_patches - len(importance)
                    extra_patches = random.sample(non_salient, extra)
                    selected_indices = extra_patches + importance
        else:
            raise ValueError(f'{patch_selection} patch selection is not supported.')

        return selected_indices

    def create_binary_mask(self, image_size, patch_size, selected_patch_indices):
        channels, height, width = image_size
        start_index = torch.tensor(sorted(selected_patch_indices)) * patch_size
        row_num = start_index // width
        row_start = row_num * patch_size
        row_end = (row_num + 1) * patch_size

        column_first = start_index % width
        column_end = column_first + patch_size

        num_patches = len(row_start)
        mask = torch.zeros((height, width), dtype=torch.bool)

        for i in range(num_patches):
            row_indices = torch.arange(row_start[i], row_end[i]).unsqueeze(1)
            col_indices = torch.arange(column_first[i], column_end[i])
            mask[row_indices, col_indices] = True
        return mask

    def calculate_blur_metric(self, patch):
        # ref: https://pyimagesearch.com/2020/06/15/opencv-fast-fourier-transform-fft-for-blur-detection-in-images-and-video-streams/
        fft_image = torch.fft.fft2(patch)
        fft_shifted = torch.fft.fftshift(fft_image)
        magnitude_spectrum = 20 * torch.log10(torch.abs(fft_shifted))
        blur_metric = torch.mean(magnitude_spectrum)
        return blur_metric

    def calculate_and_sort_blur_metrics(self, image_tensors):
        blur_metrics_with_indices = []
        for i, image in enumerate(image_tensors):
            blur_metric = self.calculate_blur_metric(image)
            # if torch.isfinite(blur_metric):
            blur_metrics_with_indices.append((blur_metric, i))

        blur_metrics_with_indices.sort(key=lambda x: x[0])
        return blur_metrics_with_indices

    def calculate_frequency(self, image_patches):
        frequencies = self.calculate_and_sort_blur_metrics(image_patches)
        return frequencies

    def calculate_entropy(self, image_tensors):
        entropy_with_indices = []
        for i, image in enumerate(image_tensors):
            flattened_image = image.reshape(-1)
            hist = torch.histc(flattened_image, bins=256, min=0, max=1)
            hist = hist / hist.sum()
            entropy = -torch.sum(hist * torch.log2(hist + 1e-9))
            entropy_with_indices.append((entropy, i))

        entropy_with_indices.sort(key=lambda x: x[0])
        return entropy_with_indices

    def calculate_gradient(self, image_tensor):
        if image_tensor.shape[0] == 3:
            image_tensor = image_tensor.mean(dim=0, keepdim=True)
        sobel_x = torch.tensor([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=torch.float32).unsqueeze(0).unsqueeze(0)
        sobel_y = torch.tensor([[1, 2, 1], [0, 0, 0], [-1, -2, -1]], dtype=torch.float32).unsqueeze(0).unsqueeze(0)
        grad_x = F.conv2d(image_tensor, sobel_x, padding=1)
        grad_y = F.conv2d(image_tensor, sobel_y, padding=1)
        grad_mag = torch.sqrt(grad_x ** 2 + grad_y ** 2)
        return torch.sum(torch.abs(grad_mag))

    def calculate_gradients(self, image_tensors):
        gradients_with_indices = []
        for i, image in enumerate(image_tensors):
            gradient = self.calculate_gradient(image)
            gradients_with_indices.append((gradient, i))

        gradients_with_indices.sort(key=lambda x: x[0])
        return gradients_with_indices

    def calculate_importance(self, patch_selection, image_patches, patch_size, patch_stride, mask=None):
        if patch_selection == 'frequency':
            importance = self.calculate_frequency(image_patches)
        elif patch_selection == 'entropy':
            importance = self.calculate_entropy(image_patches)
        elif patch_selection == 'gradient':
            importance = self.calculate_gradients(image_patches)
        elif patch_selection == 'saliency':
            mask_patches = self.image_to_patches(mask, patch_size, patch_stride)
            mask_tensors = torch.stack(mask_patches)
            mask_tensors = mask_tensors.reshape(mask_tensors.shape[0], -1)
            # salient_part = torch.any(mask_tensors != 0, dim=1)
            # salient_indices = torch.where(salient_part)[0].tolist()
            salient_part = mask_tensors.sum(1) > (mask_tensors.max() // 2)
            importance = torch.where(salient_part)[0].tolist()
        else:
            importance = [0] * len(image_patches)
        return importance

    def prepare_pos_embed_ms(self, masks, dim):
        fine_pos_embeds = []
        for i, fine_mask in enumerate(masks):
            fine_size = fine_mask.size()
            if fine_size not in self.pos_embeds:
                patch_pos_embed, class_pos_embed = self.interpolate_positional_embedding(self.pos_embed, fine_size,
                                                                                         self.interpolate_offset, dim)
                self.pos_embeds[fine_size] = torch.cat((class_pos_embed.unsqueeze(0), patch_pos_embed), dim=1)
                fine_pos_embed = patch_pos_embed[:, fine_mask.type(torch.bool).flatten(), :]
            else:
                patch_pos_embed = self.pos_embeds[fine_size][:, 1:, :]
                class_pos_embed = self.pos_embeds[fine_size][:, 0, :]
                fine_pos_embed = patch_pos_embed[:, fine_mask.type(torch.bool).flatten(), :]

            fine_pos_embeds.append(fine_pos_embed)

        fine_pos_embeds = torch.cat(fine_pos_embeds, dim=1)

        final_pos_embed = torch.cat([class_pos_embed.unsqueeze(0), fine_pos_embeds], dim=1)
        return final_pos_embed

    def random_drop(self, input, pos_embed, mask_ms=None):
        elements_to_remove = input.shape[0] - self.hidden_size
        indices_to_remove = random.sample(range(1, input.shape[0]), elements_to_remove)  # to keep the cls token
        mask = torch.ones(input.shape[0], dtype=torch.bool)
        mask[indices_to_remove] = False
        input = input[mask, :, :, :]
        pos_embed = pos_embed[mask, :]
        if mask_ms is not None:
            mask_ms = mask_ms[mask]
            return input, pos_embed, mask_ms
        else:
            return input, pos_embed

    def highResPreserve_ms(self, image, mask=None):
        image = self.pad_or_crop(image, self.lcm(self.scaled_patchsizes))
        if mask is not None:
            mask = self.pad_or_crop(mask, self.lcm(self.scaled_patchsizes))
            if mask.size()[1:] != image.size()[1:]:
                raise ValueError('Image size and mask size do not match.')

        # To make all of them a multiple of the patch size, we use the following line.
        patch_sizes = [x + (self.patch_size - x % self.patch_size) if x % self.patch_size != 0 else x for x in
                       self.scaled_patchsizes]
        patch_strides = [x + (self.patch_size - x % self.patch_size) if x % self.patch_size != 0 else x for x in
                         self.scaled_patchsizes]

        image_patches = self.image_to_patches(image, patch_sizes[-1], patch_strides[-1])

        # detecting the important indices in patches
        importance = self.calculate_importance(self.patch_selection_strategy, image_patches, patch_sizes[-1],
                                               patch_strides[-1], mask)

        n_patch_per_col = image.size()[-1] // patch_sizes[-1]
        n_patch_per_row = image.size()[-2] // patch_sizes[-1]

        ratio = 1 / self.num_scales

        n_patches = int((self.initial_hidden_size * ratio) / ((2 ** (self.num_scales - 1)) ** 2))
        # n_token_per_scale = (len(image_patches) // self.num_scales)
        # ratio_h = patch_sizes[-1] // patch_sizes[0]
        # n_patches_h = n_token_per_scale // ratio_h ** 2  # number of patches in the highest resolution
        # level n : Highest resolution : For example: 64 between 16, 32, 64
        locals()[f'selected_indices_l{self.num_scales - 1}'] = self.patch_selection(self.patch_selection_strategy,
                                                                                    importance,
                                                                                    n_patches, self.num_scales - 1,
                                                                                    range(len(image_patches)))

        # To visualize the selected area
        # transform = T.ToPILImage()
        # image_pil = transform(image)
        # output = draw_red_boundaries_on_patches(image_pil,  locals()[f'selected_indices_l{self.num_scales - 1}'], patch_sizes[-1])
        # output.show()

        locals()[f'patches_l{self.num_scales - 1}'] = []
        for i in (sorted(locals()[f'selected_indices_l{self.num_scales - 1}'])):
            patches = self.image_to_patches(image_patches[i], self.patch_size, self.patch_stride)
            locals()[f'patches_l{self.num_scales - 1}'].extend(patches)

        locals()[f'mask_l{self.num_scales - 1}'] = [self.num_scales - 1] * len(
            locals()[f'patches_l{self.num_scales - 1}'])

        # level 1 ... n - 1
        remaining_patches = range(len(image_patches))
        intermediate_patches = []
        intermediate_masks = []
        selected_indices = []
        for i in range(self.num_scales):
            if i == 0 or i == self.num_scales - 1:
                continue
            else:
                p = 0
                remaining_patches = list(
                    set(remaining_patches) - set(locals()[f'selected_indices_l{self.num_scales - 1}']))

                # ratio = patch_sizes[i] // patch_sizes[0]
                # n_patches = n_token_per_scale // ratio ** 2

                locals()[f'selected_indices_l{i}'] = self.patch_selection(self.patch_selection_strategy, importance,
                                                                          n_patches, i, remaining_patches)

                for index in sorted(locals()[f'selected_indices_l{i}']):
                    a = F.interpolate(image_patches[index].unsqueeze(0),
                                      size=(self.scaled_patchsizes[i], self.scaled_patchsizes[i]),
                                      mode='bicubic').squeeze(0)
                    patch = self.image_to_patches(a, self.patch_size, self.patch_stride)
                    intermediate_patches.extend(patch)
                    p = p + len(patch)

                locals()[f'mask_l{i}'] = [i] * p
                intermediate_masks.extend(locals()[f'mask_l{i}'])
                selected_indices.extend(locals()[f'selected_indices_l{i}'])

        selected_indices = selected_indices + locals()[f'selected_indices_l{self.num_scales - 1}']

        # Level 0
        p = 0
        selected_indices_l0 = [x for x in range(0, len(image_patches)) if
                               x not in selected_indices]
        remaining_patches = []
        for index in sorted(selected_indices_l0):
            a = F.interpolate(image_patches[index].unsqueeze(0),
                              size=(self.scaled_patchsizes[0], self.scaled_patchsizes[0]),
                              mode='bicubic').squeeze(0)
            patch = self.image_to_patches(a, self.patch_size, self.patch_stride)
            remaining_patches.extend(patch)
            p = p + len(patch)

        mask_l0 = [0] * p

        final = remaining_patches + intermediate_patches + locals()[
            f'patches_l{self.num_scales - 1}']  # level 0, ..., n

        mask_ms = mask_l0 + intermediate_masks + locals()[f'mask_l{self.num_scales - 1}']
        final = torch.stack(final)
        # print(final.size())
        # pos embed
        masks = []
        for i in range(self.num_scales):
            p = patch_sizes[i] // self.patch_size
            mask = self.create_binary_mask((3, p * n_patch_per_row, p * n_patch_per_col), p,
                                           locals()[f'selected_indices_l{i}'])
            masks.append(mask)

        pos_embeds = self.prepare_pos_embed_ms(masks, self.pos_embed.shape[-1]).squeeze(0)

        final_tensor = final

        final_tensor = torch.cat((torch.zeros(1, final_tensor.shape[1], final_tensor.shape[2], final_tensor.shape[3]),
                                  final_tensor), dim=0)  # instead of CLS token
        mask_ms.insert(0, 0)  # for cls token

        if final_tensor.shape[0] != pos_embeds.shape[0]:
            raise ValueError("Pos embedding length doesn't match the tokens length.")

        if self.without_pad_or_dropping:
            return final_tensor, pos_embeds, torch.Tensor(mask_ms)
        else:
            if final_tensor.shape[0] < self.hidden_size:
                input = self.padding(final_tensor, self.hidden_size)
                pos_embeds = self.padding(pos_embeds.unsqueeze(-1).unsqueeze(-1), self.hidden_size).squeeze(-1).squeeze(
                    -1)

                padded_area = self.hidden_size - final_tensor.shape[0]
                pad = [9] * padded_area
                mask_ms = mask_ms + pad
                mask = torch.Tensor(mask_ms)

            elif final_tensor.shape[0] > self.hidden_size:
                input, pos_embeds, mask = self.random_drop(final_tensor, pos_embeds, torch.Tensor(mask_ms))
            else:
                input = final_tensor
                mask = torch.Tensor(mask_ms)

            return input, pos_embeds, mask

    def normal_flow(self, original_image):
        original_image = self.add_padding(original_image, self.patch_size)
        channels, H, W = original_image.size()
        n_crops_w = math.ceil(W / self.patch_size)
        n_crops_H = math.ceil(H / self.patch_size)
        size = (n_crops_H, n_crops_w)
        image_patches = self.image_to_patches(original_image, self.patch_size, self.patch_stride)
        input = torch.stack(image_patches)

        # visualize_patches(image_patches, 32, 10).save(r'C:\Users\gestaltrevision\Pictures\sample_1.jpg')
        # visualize_patches(depth_patches, 32, 10).save(r'C:\Users\gestaltrevision\Pictures\sample_1_depth.jpg')

        input = torch.cat((torch.zeros(1, input.shape[1], input.shape[2], input.shape[3]),
                           input), dim=0)  # instead of CLS token

        if size not in self.pos_embeds:
            patch_pos_embed, class_pos_embed = self.interpolate_positional_embedding(self.pos_embed, size, 0.1,
                                                                                     self.pos_embed.shape[-1])
            pos_embed = torch.cat((class_pos_embed.unsqueeze(0), patch_pos_embed), dim=1)
            self.pos_embeds[size] = pos_embed
        else:
            pos_embed = self.pos_embeds[size]

        pos_embed = pos_embed.squeeze(0)
        if input.shape[0] != pos_embed.shape[0]:
            raise ValueError("Pos embedding length doesn't match the tokens length.")

        if self.without_pad_or_dropping:
            mask = torch.zeros(input.shape[0])
            return input, pos_embed, mask
        else:
            if input.shape[0] < self.hidden_size:
                mask = torch.zeros(input.shape[0])
                padded_area = self.hidden_size - input.shape[0]
                pad = [9] * padded_area
                mask = torch.cat((mask, torch.Tensor(pad)), 0)
                input = self.padding(input, self.hidden_size)
                pos_embed = self.padding(pos_embed.unsqueeze(-1).unsqueeze(-1), self.hidden_size).squeeze(-1).squeeze(
                    -1)
            elif input.shape[0] > self.hidden_size:
                input, pos_embed = self.random_drop(input, pos_embed)
                # input = input[:self.hidden_size, :, :, :]
                # pos_embed = pos_embed[:self.hidden_size, :]
                mask = torch.zeros(self.hidden_size)
            else:
                mask = torch.zeros(self.hidden_size)

        return input, pos_embed, mask

    def preprare_patches(self, original_image, saliency_mask=None):
        channels, H, W = original_image.size()
        n_crops_w = math.ceil(W / self.patch_size)
        n_crops_H = math.ceil(H / self.patch_size)
        if n_crops_H * n_crops_w <= self.hidden_size:
            input, pos_embed, mask = self.normal_flow(original_image)
        else:
            input, pos_embed, mask = self.highResPreserve_ms(original_image, saliency_mask)
        return input, pos_embed, mask

    def preprocess(self, img_path, mask_path=None):
        image_pil = Image.open(img_path)
        image_pil = image_pil.convert("RGB")
        # print(f'Image size: {image_pil.size}')

        if self.patch_selection_strategy == 'saliency':
            mask = Image.open(mask_path)
            mask = mask.convert("L")
            mask = mask.point(lambda p: 255 if p > 0.5 else 0)  # making the mask binary
        else:
            mask = None

        if self.dataset == 'para' or self.dataset == 'spaq':
            width, height = image_pil.size
            if max(width, height) > 1024:
                max_size = 1024
                ratio = min(max_size / width, max_size / height)

                new_width = int(width * ratio)
                new_height = int(height * ratio)

                image_pil = image_pil.resize((new_width, new_height))
                if self.patch_selection_strategy == 'saliency':
                    mask = mask.resize((new_width, new_height))

        image = transforms.ToTensor()(image_pil)

        if self.patch_selection_strategy == 'saliency':
            mask = transforms.ToTensor()(mask)

            if image.shape[1:] != mask.shape[1:]:
                raise Exception('Image and Depth map should have the same size !')

        if self.patch_selection_strategy == 'original':
            input = self.resize(image)
            input, _ = self.random_crop(input)
            pos_embed = torch.tensor([])
            mask_tokens = torch.tensor([])
        else:
            input, pos_embed, mask_tokens = self.preprare_patches(image, mask)

        return input, pos_embed, mask_tokens
