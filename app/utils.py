import matplotlib.pyplot as plt

def print_layer(x, l):
    plt.figure(figsize=(18, 16), dpi=80, facecolor='w', edgecolor='k')

    out = x.squeeze()
    if len(out.shape) < 2: return

    f, w, h = out.shape

    plt.title(l)

    for i, img in enumerate(out):
        img = img.detach().numpy()
        plt.subplot(1, 6, i + 1)
        plt.imshow(img)
        if i > 4:
            break

    plt.show()