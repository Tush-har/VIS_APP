def voc_to_yolo(bbox, img_w, img_h):
    xmin, ymin, xmax, ymax = bbox

    x_center = ((xmin + xmax) / 2) / img_w
    y_center = ((ymin + ymax) / 2) / img_h
    width = (xmax - xmin) / img_w
    height = (ymax - ymin) / img_h

    return x_center, y_center, width, height
