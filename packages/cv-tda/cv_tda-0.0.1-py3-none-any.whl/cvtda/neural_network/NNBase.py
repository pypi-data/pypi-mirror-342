import torch
import torchph.nn.slayer
import torchvision.models


class NNBase(torch.nn.Module):
    def __init__(
        self,

        num_diagrams: int,
        skip_diagrams: bool = False,
        features_per_diagram: int = 64,

        skip_images: bool = False,
        images_n_channels: int = 3,
        images_output: int = 1024,

        skip_features: bool = False,
        features_output: int = 1024
    ):
        super().__init__()
        
        def make_slayer():
            return torchph.nn.slayer.SLayerExponential(features_per_diagram)
        self.slayers_ = None if skip_diagrams else torch.nn.ModuleList([ make_slayer() for _ in range(num_diagrams) ])
        self.slayers_compressor_ = torch.nn.Linear(num_diagrams * features_per_diagram, features_output)

        self.images_ = None
        if not skip_images:
            self.images_ = torchvision.models.resnet50(num_classes = images_output)
            self.images_.conv1 = torch.nn.Conv2d(images_n_channels, 64, kernel_size = 7, stride = 2, padding = 3, bias = False)

        self.features_ = None if skip_features else torch.nn.LazyLinear(features_output)
    
    def forward(self, images, features, *diagrams):
        result = [ ]
        
        if self.images_ is not None:
            result.append(self.images_(images))

        if self.slayers_ is not None:
            result.append(
                self.slayers_compressor_(
                    torch.cat([
                        self.slayers_[i]((diagrams[2 * i], diagrams[2 * i + 1], diagrams[2 * i].shape[1], len(images)))
                        for i in range(len(self.slayers_))
                    ], dim = 1)
                )
            )
    
        if self.features_ is not None:
            result.append(self.features_(features))

        return torch.cat(result, dim = 1)
