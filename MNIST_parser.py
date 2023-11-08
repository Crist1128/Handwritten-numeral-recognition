import os, codecs, numpy, gzip, shutil, cv2

# GET DIRECTORY WITH THE EXTRACTED FILES FROM USER INPUT
datapath = input("Enter the path to the directory containing the MNIST dataset: ")

if os.path.isdir(datapath):
    pass
else:
    print("Input path error!!!")
    exit()

# LISTING ALL ARCHIVES IN THE DIRECTORY
files = os.listdir(datapath)
for file in files:
    if file.endswith('gz'):
        print('Extracting ',file)
        with gzip.open(os.path.join(datapath, file), 'rb') as f_in:
            with open(os.path.join(datapath, file.split('.')[0]), 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
print('Extraction Complete')

files = os.listdir(datapath)

def get_int(b):   # CONVERTS 4 BYTES TO AN INT
    return int(codecs.encode(b, 'hex'), 16)

data_dict = {}
for file in files:
    if file.endswith('ubyte'):  # FOR ALL 'ubyte' FILES
        print('Reading ',file)
        with open(os.path.join(datapath, file), 'rb') as f:
            data = f.read()
            type = get_int(data[:4])   # 0-3: THE MAGIC NUMBER TO WHETHER IMAGE OR LABEL
            length = get_int(data[4:8])  # 4-7: LENGTH OF THE ARRAY  (DIMENSION 0)
            if (type == 2051):
                category = 'images'
                num_rows = get_int(data[8:12])  # NUMBER OF ROWS  (DIMENSION 1)
                num_cols = get_int(data[12:16])  # NUMBER OF COLUMNS  (DIMENSION 2)
                parsed = numpy.frombuffer(data, dtype=numpy.uint8, offset=16)  # READ THE PIXEL VALUES AS INTEGERS
                parsed = parsed.reshape(length, num_rows, num_cols)  # RESHAPE THE ARRAY AS [NO_OF_SAMPLES x HEIGHT x WIDTH]           
            elif(type == 2049):
                category = 'labels'
                parsed = numpy.frombuffer(data, dtype=numpy.uint8, offset=8)  # READ THE LABEL VALUES AS INTEGERS
                parsed = parsed.reshape(length)  # RESHAPE THE ARRAY AS [NO_OF_SAMPLES]                           
            if (length == 10000):
                set_name = 'test'
            elif (length == 60000):
                set_name = 'train'
            data_dict[set_name + '_' + category] = parsed  # SAVE THE NUMPY ARRAY TO A CORRESPONDING KEY     

sets = ['train', 'test']

for set_name in sets:   # FOR TRAIN AND TEST SET
    images = data_dict[set_name + '_images']   # IMAGES
    labels = data_dict[set_name + '_labels']   # LABELS
    no_of_samples = images.shape[0]     # NUMBER OF SAMPLES
    for indx in range(no_of_samples):  # FOR EVERY SAMPLE
        print(set_name, indx)
        image = images[indx]            # GET IMAGE
        label = labels[indx]            # GET LABEL
        if not os.path.exists(os.path.join(datapath, set_name, str(label))):
            os.makedirs(os.path.join(datapath, set_name, str(label)))  # CREATE TRAIN/TEST DIRECTORY AND CLASS-SPECIFIC SUBDIRECTORY
        filenumber = len(os.listdir(os.path.join(datapath, set_name, str(label)))) # NUMBER OF FILES IN THE DIRECTORY FOR NAMING THE FILE
        cv2.imwrite(os.path.join(datapath, set_name, str(label), '%05d.png' % (filenumber)), image)  # SAVE THE IMAGE WITH PROPER NAME
