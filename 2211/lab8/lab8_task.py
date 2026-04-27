# %% [markdown]
# # COMP 2211
# ## Lab 8: Convolutional Neural Network (CNN)
# 
# The German Traffic Sign Recognition Benchmark (GTSRB) is a real-world image dataset designed to evaluate how well machine learning models can recognize traffic signs from camera images. It contains more than 50,000 labeled images of German road signs belonging to 43 different classes, such as speed limits, warning signs, and mandatory actions, collected under varied conditions (different lighting, distances, and viewing angles). The dataset was originally created for a multi-class image classification competition at IJCNN 2011 and has since become a standard benchmark for testing convolutional neural networks on traffic sign recognition tasks.
# 
# In your lab, students will use GTSRB to train a CNN that takes a single traffic sign image as input and predicts which sign class it belongs to. This makes the task directly relevant to autonomous driving and advanced driver-assistance systems, where reliable automatic understanding of traffic signs is safety‑critical. Since the original dataset is quite large, for this lab we will use a reduced version of the dataset, containing 5 classes and 2210 images. 
# 
# For this lab, you will need to implement 2 tasks. The first one will be to complete the train_test_split function, and the second one will be to implement your CNN model in def_build function. The point distribution for this task will be as follows:
# 
# 1. Test #1: function train_test_split (2.5 points)
# 2. Test #2: Above 0.70 accuracy on hidden test case (2.5 points)
# 3. Test #3: Above 0.80 accuracy on hidden test case (2.5 points)
# 4. Test #4: Above 0.95 accuracy on hidden test case (2.5 points)

# %% [markdown]
# ## **Data Preparation**
# 
# 
# 1. Download the dataset from [here](https://course.cse.ust.hk/comp2211/labs/lab8/files/lab8_Fall2025_train.zip).
# 2. Upload this data to your Google Drive, under folder `comp2211/lab8`.
# 3. Run the following code cell to mount Google Drive and unzip the data.
# 
# Note: If this lasts for more than three minutes, you may try deleting the previously unzipped folder on Google Drive and try again.
# 
# 

# %%
if __name__ == "__main__":
  from google.colab import drive
  import subprocess
  import os
  drive.mount("/content/drive")
  # Change working directory
  os.chdir("/content/drive/MyDrive/comp2211/lab8/")

  # Unzip the file 'lab8_Fall2025_train.zip' into the current directory
  zip_path = "lab8_train.zip"
  subprocess.run(["unzip", "-q", "-o", zip_path, "-d", "."], check=True)

# %% [markdown]
# ## **Dataset Construction**
# 
# First, we prepare the dataset for visualization and CNN model from our image directory.  

# %%
from PIL import Image
def prepare_dataset(directory):
    import os 
    import numpy as np 
    
    data = []
    labels = []
    classes = 5

    cur_path = directory

    for i in range(classes):
        path = os.path.join(cur_path, "Train", str(i))
        images = os.listdir(path)

        for a in images: 
            try:
                image = Image.open(path + '/' + a)
                image = image.resize((30, 30))
                image = np.array(image)
                data.append(image)
                labels.append(i)

            except:
                print(f"Error loading image: {a}")

    data = np.array(data)
    labels = np.array(labels)

    return data,labels

# %%
if __name__ == "__main__":
    import os
    directory = os.getcwd()
    data, labels = prepare_dataset(directory)
    # print(data)
    print(f"Data shape: {data[0].shape} \nTotal images: {labels.shape}")

# %% [markdown]
# ## **Data Preparation** 
# 

# %% [markdown]
# ### **Data Normalization & Train-validation split**
# 
# Before your CNN can learn traffic sign patterns, the raw dataset needs two critical preprocessing steps:
# 
# 1. Train-Test Split: Prevents data leakage and enables proper model evaluation
# 2. Normalization: Ensures stable, fast training by scaling pixel values properly
# 
# If you train AND test on the same data, you'll get unrealistically perfect scores (100% accuracy!). Real-world models must predict unseen examples.
# 
# Also, Raw pixels range from [0, 255] (int8). Neural networks expect normalized inputs in [0, 1] (float32).
# 
# 

# %% [markdown]
# ## **Task 1: Data Split**
# 
# For this task, you will split the dataset into 75% training dataset and 25% validation set. Data normalization and one-hot encoding have already been done for you.
# 
# You may consider using one of the following utilities for the split:
# 
# - `sklearn.model_selection.train_test_split`
# - `keras.utils.split_dataset`

# %%
def train_test_split(directory):
    # we have not imported the above libaries and functions

    '''
    Task 1: you need to split the full dataset into training and validation sets.
    It is crucial to have a separate validation set from the training set,
    as you will need to evaluate each new model using the validation set.
    Evaluating on the test set is not advisable, as it can lead to cherry-picking results.
    For instance, you might select different random seeds and choose the one that
    yields the highest accuracy on the test set. However, this approach does not
    contribute to developing better models, and we should avoid such practices.
    '''
    
    ''' 
    Split the dataset into training data (X_train, y_train) and validation data (X_val, y_val). We expect 1650 images
    to be used for training and 550 for validation.
    '''

    X_data, y_labels = prepare_dataset(directory)
    
    X_data = X_data.astype('float32')/255.0
    y_labels = y_labels 
    
    X_train = None
    X_val = None
    y_train = None
    y_val = None

    # Task 1: Your code here 
    from sklearn.model_selection import train_test_split
    
    X_train, X_val, y_train, y_val = train_test_split(
        X_data, 
        y_labels, 
        test_size=0.25,  # 25% validation = 550 images
        random_state=42, # Fixed seed 
        stratify=y_labels 
    )
    

    # End Task

    # One-Hot Encoding for the labels
    from keras.utils import to_categorical

    y_train = to_categorical(y_train, 5)
    y_val = to_categorical(y_val, 5)

    return X_train, X_val, y_train, y_val


# %%
if __name__ == "__main__": 

    X_train, X_val, y_train, y_val = train_test_split(directory) 
    print(f"Final Training shape: {X_train.shape}")
    print(f"Final Validation shape: {X_val.shape}")

# %%


# %% [markdown]
# ## **Task 2: Build the Model**

# %% [markdown]
# For this task, you will need to build a CNN model to predict the class each image belongs
# to. The model shall output an array equivalent of length 5, where each value
# corresponds to the possibility of the image belongs to each class. Your model shall
# consist of at least one Conv2D layer and at least one Dense layer. Use activation
# functions as appropriate and pay special attention to the last layer's activation.
# 
# For your reference, our model has only around 50,000 parameters. In our model,
# we used the following layers:
# 
# Conv2D https://www.tensorflow.org/api_docs/python/tf/keras/layers/Conv2D
# 
# Dropout https://www.tensorflow.org/api_docs/python/tf/keras/layers/Dropout
# 
# MaxPooling2D https://www.tensorflow.org/api_docs/python/tf/keras/layers/MaxPool2D
# 
# Dense https://www.tensorflow.org/api_docs/python/tf/keras/layers/Dense
# 
# Feel free to explore other layers in tensorflow package if you want. Please
# do not come up with a very large model with very large number of parameters, although
# your marks will not be deducted as long as it can pass the test on ZINC
# 
# You will be scored on our own private test case. To achieve maximum score, you must score an accuracy above 0.95. We know it seems high, but do not worry! As long as your validation accuracy is high enough (> 96%), you will be able to pass the test.  

# %%

def build_model():

    '''
    Task 2: Build your CNN model here  
    '''
    
    import tensorflow as tf

    model = None 

    # Task 2: Your code here

    model = tf.keras.Sequential([
        # First Convolution Block
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(30, 30, 3)),
        tf.keras.layers.MaxPooling2D((2, 2)),
        
        # Second Convolution Block
        tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D((2, 2)),
        
        # Third Convolution Block (EXTRA ONE = better features)
        tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D((2, 2)),
        
        # Prevent overfitting
        tf.keras.layers.Dropout(0.3),
        
        # Prepare for MLP
        tf.keras.layers.Flatten(),
        
        # Dense layer (brain)
        tf.keras.layers.Dense(128, activation='relu'),
        
        # Final 5-class probabilities
        tf.keras.layers.Dense(5, activation='softmax')
    ])



    # End Task 

    return model


# %%
if __name__ == "__main__": 
    model = build_model()
    model.compile(
        optimizer = "adam", 
        loss = "categorical_crossentropy",
        metrics = ["accuracy"]
    )

    model.summary()

# %% [markdown]
# ## **Training log visualization**

# %%


# %%
if __name__ == "__main__":
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'], label='Train accuracy')
    plt.plot(history.history['val_accuracy'], label='Validation accuracy')
    plt.title('Model Accuracy')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.legend()

# %% [markdown]
# ## **Evaluate the Model**
# 
# Make sure you are able to run the model properly. Otherwise, it might affect your score. 

# %%
from keras.models import load_model

if __name__ == "__main__":
    model = load_model('model_lab8.keras')          # Restore the best model
    val_loss, val_acc = model.evaluate(X_val, y_val)
    print('Validation loss: {}'.format(val_loss))
    print('Validation accuracy: {}'.format(val_acc))

# %% [markdown]
# ## **Submission and Grading**
# 
# 1. Save your Python Notebook as a lab8_task.py file from Google Colab by clicking File -> Download -> Download .py.
# 2. Download your trained model model_lab8.keras.
# 3. Submit lab8_task.py and your trained model model_lab8.keras to ZINC. 

# %% [markdown]
# 

# %% [markdown]
# 

# %% [markdown]
# 

# %% [markdown]
# 


