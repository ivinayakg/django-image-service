import cv2

def query_decrypt(query):
    query_options = ['h', 'w', 'r', 'c']
    result = {}
    for x in query.split('__'):
        option = x.split('_')
        if option[0] in query_options:
            result[option[0]] = option[1]
    
    return result

def query_image_generator(image, query, image_name):
    src_image = cv2.imread(image, cv2.IMREAD_UNCHANGED)
    image_path = image.split('images/')
    new_image_name = image_name + '.'+ image_path[1].split('.')[1]
    if 'h' in query and 'w' in query:
        dsize = (int(query.get('w')), int(query.get('h')))
        output = cv2.resize(src=src_image, dsize=dsize)
    new_image_path = image_path[0]+ 'images/' + new_image_name 
    cv2.imwrite(new_image_path, output)

    return (new_image_path, new_image_name)
        