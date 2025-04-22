import torch
import torch.nn as nn
from transformers import ViTModel, AutoModel
import numpy as np
import warnings

warnings.filterwarnings('ignore')

class ScaleEmbs(nn.Module):
    """Adds learnable scale embeddings to the inputs."""

    def __init__(self, num_scales, hidden_size):
        super(ScaleEmbs, self).__init__()
        self.scale_emb_init = nn.init.normal_
        self.se = self.initialization(num_scales, hidden_size)

    def initialization(self, num_scales, hidden_size):
        se = nn.Parameter(torch.empty((1, num_scales, hidden_size)))
        se = self.scale_emb_init(se, mean=0.0, std=0.02)
        se = se.detach().numpy()
        return se

    def forward(self, inputs_positions):
        selected_pe = np.take(self.se[0], inputs_positions.unsqueeze(0), axis=0)
        return torch.tensor(selected_pe)


class PatchEmbeddings(nn.Module):
    def __init__(self, patch_selection,patch_size, hidden_size, scales=2, encoder_name = 'facebook/dinov2-small'):
        super().__init__()
        self.patch_selection = patch_selection
        self.scales = scales
        self.encoder_name = encoder_name
        self.patch_size = patch_size
        if "dino" in encoder_name:
            model = AutoModel.from_pretrained(encoder_name)
            self.cls_token = model.embeddings.cls_token
        else:
            model = ViTModel.from_pretrained(encoder_name)
            self.cls_token = model.embeddings.cls_token

        if self.patch_selection == 'original':
            self.patch_embedder = model.embeddings.patch_embeddings
        else:
            self.se = self.se_initialization(self.scales, model.embeddings.position_embeddings.shape[-1])  # scale embeddings
            self.mask_token = nn.Parameter(torch.zeros(1, 1, hidden_size))

            self.patch_embedder = model.embeddings.patch_embeddings.projection

    def se_initialization(self, scales, size):
        se = nn.Parameter(torch.empty((1, scales, size)))  # scale embedding
        se = nn.init.normal_(se, mean=0.0, std=0.02)
        return se

    def add_scale_embed(self, input, masks):
        np_se = self.se.detach().cpu().numpy()[0]
        mask = masks[:, 1:].unsqueeze(0).cpu()
        scale_embed = torch.tensor(np.take(np_se, mask, axis=0)).to(input.device)[0]
        input = input + scale_embed
        return input

    def forward(self, patches, pos_embeds, masks):

        if self.patch_selection == 'original':
            embedding = self.patch_embedder(patches)
        else:
            patches = patches[:, 1:, :, :, :]  # remove the zero padding for the cls token
            batch_size, l, c, W, H = patches.size()

            patches = patches.reshape(-1, c, W, H)

            embedding = self.patch_embedder(patches)
            embedding = embedding.reshape(batch_size, l, -1)

            if masks is not None:
                padding_mask = (masks == 9).int()
                masks[masks == 9] = 0  # similar to the MUSIQ paper
                seq_length = embedding.shape[1]
                mask_tokens = self.mask_token.expand(batch_size, seq_length, -1)
                # replace the masked visual tokens by mask_tokens
                mask = padding_mask[:, 1:].unsqueeze(-1).type_as(mask_tokens)
                embedding = embedding * (1.0 - mask) + mask_tokens * mask

            if self.scales != 1:
                embedding = self.add_scale_embed(embedding, masks)
            cls_token = self.cls_token.expand(batch_size, -1, -1)
            embedding = torch.cat((cls_token, embedding), dim=1)
            embedding = embedding + pos_embeds

        return embedding


class Transformer(nn.Module):
    def __init__(self, encoder_name='facebook/dinov2-small'):
        super().__init__()
        if "dino" in encoder_name:
            model = AutoModel.from_pretrained(encoder_name)
            self.encoder = model.encoder
            self.layernorm = model.layernorm
        elif "vit" in encoder_name:
            model = ViTModel.from_pretrained(encoder_name)
            self.encoder = model.encoder
            self.layernorm = model.layernorm
        else:
            raise ValueError("Model is not supported.")

    def forward(self, encoder_input):
        encoder_output = self.encoder(encoder_input).last_hidden_state
        encoder_output = self.layernorm(encoder_output)
        return encoder_output


class MlpHead(nn.Module):
    def __init__(self, hidden_size, data, num_classes):
        super().__init__()
        self.linear = nn.Linear(hidden_size * 2, num_classes)
        self.dropout = nn.Dropout(p=0)
        if data == 'ava' or data == 'para':
            self.activation = nn.Softmax(dim=-1)
            self.multi = False
        elif data == 'aadb':
            self.activation = nn.Sigmoid()
            self.multi = False
        else:
            self.activation = nn.Sigmoid()
            self.multi = False

    def forward(self, hidden_states):
        cls_token_output = hidden_states[:, 0, :]
        patch_tokens = hidden_states[:, 1:, :]
        linear_input = torch.cat([cls_token_output, patch_tokens.mean(dim=1)], dim=1)
        linear_input = self.dropout(linear_input)
        linear_head = self.linear(linear_input)
        predictions = self.activation(linear_head)
        return predictions


class Model(torch.nn.Module):

    def __init__(self, dataset, patch_selection, encoder_name='facebook/dinov2-small'):
        super(Model, self).__init__()
        self.dataset = dataset
        self.model = encoder_name
        self.prepare_config()
        self.patch_selection = patch_selection
        self.patch_embeddings = PatchEmbeddings(patch_selection, self.patch_size, self.hidden_size, scales=2, encoder_name='facebook/dinov2-small')
        self.encoder = Transformer(encoder_name)
        self.mlp_head = MlpHead(self.hidden_size, dataset, self.num_classes)

    def prepare_config(self):
        if self.dataset == 'ava':
            self.hidden_size = 512
        elif self.dataset == 'tad66k':
            self.hidden_size = 768
        else:
            # print('Max number of tokens is set to 1024.')
            self.hidden_size = 1024
        self.hidden_size = self.hidden_size + 1

        if 'dino' in self.model:
            self.patch_size = 14
            self.patch_stride = 14
        else:
            ValueError(
                'Only Dinov2-small is supported in the library. For other models check our Github.')

        if self.dataset == 'ava':
            self.num_classes = 10
        elif self.dataset == 'para':
            self.num_classes = 9
        else:
            self.num_classes = 1


    def forward(self, patches, pos_embeds, masks):
        embedding = self.patch_embeddings(patches, pos_embeds, masks)
        encoder_output = self.encoder(embedding)
        predictions = self.mlp_head(encoder_output)

        return predictions
