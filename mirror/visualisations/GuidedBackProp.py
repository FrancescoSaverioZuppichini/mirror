"""
Created on Thu Oct 26 11:23:47 2017

@author: Utku Ozbulak - github.com/utkuozbulak
"""
import torch
from torch.nn import ReLU
from .Visualisation import Visualisation

from .misc_functions import (get_params,
                            convert_to_grayscale,
                            save_gradient_images,
                            get_positive_negative_saliency)

from torch.autograd import Variable

class GuidedBackprop(Visualisation):
    """
       Produces gradients generated with guided back propagation from the given image
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gradients = None
        # Put model in evaluation mode
        self.model = self.module #TODO
        self.model.eval()

        self.target_class=56

    @property
    def name(self):
        return 'guided backprop'
    def hook_layers(self):
        def hook_function(module, grad_in, grad_out):
            print('*******')
            self.gradients = grad_in[0]
        # Register hook to the first layer
        first_layer = self.tracer.operations[0][0]
        return first_layer.register_backward_hook(hook_function)

    def update_relus(self):
        """
            Updates relu activation functions so that it only returns positive gradients
        """
        def relu_hook_function(module, grad_in, grad_out):
            """
            If there is a negative gradient, changes it to zero
            """
            if isinstance(module, ReLU):
                return (torch.clamp(grad_in[0], min=0.0),)
        # Loop through layers, hook up ReLUs with relu_hook_function
        handles = []
        for pos, module in self.model._modules.items():
            if isinstance(module, ReLU):
                handles.append(module.register_backward_hook(relu_hook_function))
        return handles

    def __call__(self, input_image, layer):
        # Forward pass
        input_image_g = Variable(input_image, requires_grad=True).to(self.device)
        model_output =self.model(input_image_g)
        self.layer = layer
        # Zero gradients
        self.model.zero_grad()
        handles = self.update_relus()
        handle = self.hook_layers()
        # Target for backprop
        one_hot_output = Variable(torch.FloatTensor(1, model_output.size()[-1]).zero_(), requires_grad=True).to(self.device)
        one_hot_output[0][self.target_class] = 1
        # Backward pass
        model_output.backward(gradient=one_hot_output)
        # Convert Pytorch variable to numpy array
        # [0] to get rid of the first channel (1,3,224,224)
        gradients_as_arr = self.gradients.data.cpu().numpy()[0]
        grayscale_guided_grads = convert_to_grayscale(gradients_as_arr)
        image = torch.from_numpy(grayscale_guided_grads)
        handle.remove()
        [h.remove() for h in handles]
        print(image.shape)
        # handle.remove()
        return image.unsqueeze(0)


if __name__ == '__main__':
    target_example = 0  # Snake
    (original_image, prep_img, target_class, file_name_to_export, pretrained_model) =\
        get_params(target_example)

    # Guided backprop
    GBP = GuidedBackprop(pretrained_model)
    # Get gradients
    guided_grads = GBP.generate_gradients(prep_img, target_class)
    # Save colored gradients
    save_gradient_images(guided_grads, file_name_to_export + '_Guided_BP_color')
    # Convert to grayscale
    grayscale_guided_grads = convert_to_grayscale(guided_grads)
    # Save grayscale gradients
    save_gradient_images(grayscale_guided_grads, file_name_to_export + '_Guided_BP_gray')
    # Positive and negative saliency maps
    pos_sal, neg_sal = get_positive_negative_saliency(guided_grads)
    save_gradient_images(pos_sal, file_name_to_export + '_pos_sal')
    save_gradient_images(neg_sal, file_name_to_export + '_neg_sal')
    print('Guided backprop completed')
