Config = {



    'num_classes': 4,










    'min_dim': 300,
    'feature_maps': {
        'vgg'       : [38, 19, 10, 5, 3, 1],
        'mobilenet' : [19, 10, 5, 3, 2, 1],
    },














    'min_sizes': [30, 60, 111, 162, 213, 264],
    'max_sizes': [60, 111, 162, 213, 264, 315],
    
    'aspect_ratios': {
        'vgg'       : [[2], [2, 3], [2, 3], [2, 3], [2], [2]],
        'mobilenet' : [[2, 3], [2, 3], [2, 3], [2, 3], [2, 3], [2, 3]]
    },
    'variance': [0.1, 0.2],
    'clip': True,
}
