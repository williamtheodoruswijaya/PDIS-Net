TRAINED_MODELS = [
    # arch,       backbone,    init,       folder
    ("segformer", "mit_b0",    "imagenet", "12-segformer-mitb0-imagenet/v2"),
    ("segformer", "mit_b3",    "raw",      "01-segformer-mitb3-raw/v1"),
    ("segformer", "mit_b3",    "imagenet", "02-segformer-mitb3-imagenet/v4-final"),
    ("segformer", "mit_b3",    "aerial",   "04-segformer-mitb3-aerial/v1"),
    ("segformer", "mit_b3",    "ade",      "05-segformer-mitb3-ade/v1"),
    ("segformer", "mit_b3",    "drone",    "06-segformer-mitb3-drone/v1"),
    ("segformer", "mit_b5",    "imagenet", "07-segformer-mitb5-imagenet/v1"),
    ("segformer", "resnet34",  "raw",      "11-segformer-resnet34-raw/v2"),
    ("segformer", "resnet34",  "imagenet", "10-segformer-resnet34-imagenet/v1"),
    ("unet",      "resnet34",  "raw",      "08-unet-resnet34-raw/v1"),
    ("unet",      "resnet34",  "imagenet", "09-unet-resnet34-imagenet/v1"),
    ("deeplab",   "mit_b3",    "imagenet", "13-deeplabv3plus-mitb3-imagenet/v2"),
    ("deeplab",   "resnet34",  "raw",      "15-deeplabv3plus-resnet34-raw/v2"),
    ("deeplab",   "resnet34",  "imagenet", "14-deeplabv3plus-resnet34-imagenet/v2"),
    ("deeplab",   "resnet50",  "imagenet", "16-deeplab-resnet50-imagenet-v1"),
    ("deeplab",   "resnet101", "imagenet", "17-deeplab-resnet101-imagenet/v1"),
]

MODELS = {
    f"{arch}-{backbone}-{init}": {"arch": arch, "backbone": backbone, "init": init, "folder": folder}
    for arch, backbone, init, folder in TRAINED_MODELS
}