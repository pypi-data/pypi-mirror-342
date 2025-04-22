from huggingface_hub import hf_hub_download
import torch
import sys
import os

source_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, source_root)


class backbone(torch.nn.Module):
    """
    Backbone module for predicting the aesthetic value of images preprocessed by the Charm Tokenizer.

    Args:
        training_dataset (str): The dataset the network is pretrained on,
            used to select the appropriate pretrained model (default: 'aadb').
        device (str): The computing device to use ('cpu' or 'cuda') (default: 'cpu').
    """

    def __init__(self, training_dataset='aadb', device='cpu'):
        super(backbone, self).__init__()
        self.device = device
        self.dataset = training_dataset
        self.model = self.load_model()
        self.config_correction()
        self.range_definition()

    def mean_score(self, preds):
        if self.dataset == 'para':
            score_values = torch.arange(1, 5.5, step=0.5, dtype=torch.float32, device=self.device)
        else:
            score_values = torch.arange(1, 11, dtype=torch.float32, device=self.device)

        final_score = torch.sum(preds * score_values, dim=-1)
        return final_score

    def load_model(self):
        if self.dataset == 'aadb':
            file_name = "aadb_charm.pth"
        elif self.dataset == 'ava':
            file_name = 'Ava_large_charm.pth'
        elif self.dataset == 'para':
            file_name = "para_charm.pth"
        elif self.dataset == 'baid':
            file_name = "baid_charm.pth"
        elif self.dataset == 'koniq10k':
            file_name = "koniq10k_charm.pth"
        elif self.dataset == 'spaq':
            file_name = "spaq_charm.pth"
        elif self.dataset == 'tad66k':
            file_name = "tad66k_charm.pth"
        else:
            ValueError('Cannot find the checkpoint.')
        model_path = hf_hub_download(repo_id="FatemehBehrad/Charm", filename=file_name)
        model = torch.load(model_path, weights_only=False, map_location=self.device)['model_state_dict']
        return model

    def config_correction(self):
        self.model.patch_embeddings.scales = 2

    def range_definition(self):
        if self.dataset == 'tad66k':
            self.start = 1
            self.end = 10
        elif self.dataset == 'para':
            self.start = 0
            self.end = 5
        elif self.dataset == 'ava':
            self.start = 0
            self.end = 10
        else:
            self.start = 0
            self.end = 1

    def predict(self, tokens, pos_embed, mask_token):
        self.model = self.model.to(self.device)
        self.model.eval()

        prediction = self.model(tokens.unsqueeze(0).to(self.device), pos_embed.unsqueeze(0).to(self.device),
                                mask_token.unsqueeze(0).to(self.device))
        if self.dataset in ['ava', 'para']:
            score = self.mean_score(prediction)
        else:
            score = prediction

        score = round(float(score[0]), 3)
        print(f'Prediction: {score} from {self.start} to {self.end}')
        return score




