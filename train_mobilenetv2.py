import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam

# Image size and batch
IMG_SIZE = 224
BATCH = 32
EPOCHS = 15  # adjust for demo

# Data augmentation
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=25,
    width_shift_range=0.15,
    height_shift_range=0.15,
    shear_range=0.15,
    zoom_range=0.2,
    horizontal_flip=True,
    brightness_range=(0.7,1.3)
)

val_datagen = ImageDataGenerator(rescale=1./255)

# Load training and validation data
train_gen = train_datagen.flow_from_directory(
    'dataset/train',
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH,
    class_mode='categorical'
)

val_gen = val_datagen.flow_from_directory(
    'dataset/val',
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH,
    class_mode='categorical'
)

# Load MobileNetV2 pretrained on ImageNet
base = MobileNetV2(weights='imagenet', include_top=False, input_shape=(IMG_SIZE, IMG_SIZE, 3))
x = base.output
x = GlobalAveragePooling2D()(x)
x = Dropout(0.4)(x)
preds = Dense(2, activation='softmax')(x)  # 2 classes: cattle and buffalo
model = Model(inputs=base.input, outputs=preds)

# Freeze base layers
for layer in base.layers:
    layer.trainable = False

# Compile and train
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(train_gen, validation_data=val_gen, epochs=5)

# Unfreeze last 40 layers and fine-tune
for layer in base.layers[-40:]:
    layer.trainable = True

model.compile(optimizer=Adam(1e-5), loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(train_gen, validation_data=val_gen, epochs=EPOCHS)

# Save the trained model
model.save('model/mobilenetv2_cattle_buffalo.h5')
print("Model saved at model/mobilenetv2_cattle_buffalo.h5")