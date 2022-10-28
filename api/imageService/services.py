import cv2

def query_decrypt(query):
    query_options = ['h', 'w', 'r', 'c']
    result = {}
    for x in query.split('__'):
        option = x.split('_')
        if option[0] in query_options:
            result[option[0]] = option[1]
    
    return result

def query_image_generator(image, query, query_str):
    src_image = cv2.imread(image, cv2.IMREAD_UNCHANGED)
    image_name = image.split('.')
    if 'h' in query and 'w' in query:
        dsize = (int(query.get('w')), int(query.get('h')))
        output = cv2.resize(src=src_image, dsize=dsize)
    new_image_path = image_name[0]+ '-' + query_str+ '.'+ image_name[1]
    new_image_extension = image_name[1]
    cv2.imwrite(new_image_path, output)

    return (new_image_path, new_image_extension)
        