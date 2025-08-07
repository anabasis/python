# [01] CNN 기반의 모델 제작, 이미지 인식을 통한 영화배우 정보 조회하기

## [01] CNN 기반의 모델 제작, 이미지 인식을 통한 영화배우 정보 조회하기

### 1. 학습 데이터 전처리

1) 자신이 관심있는 영화배우 이미지를 선정하여 저장
/ws_python/notebook/machine/cnn_actor
├─train
│  ├─Amanda Seyfried     ◀─ 35개 이미지
│  ├─Andrew Lincoln
│  ├─Anne Hathaway
│  ├─Keira Christina Knightley
│  └─Pierce Brosnan
├─validation
│  ├─Amanda Seyfried     ◀─ 10개 이미지
│  ├─Andrew Lincoln
│  ├─Anne Hathaway
│  ├─Keira Christina Knightley
│  └─Pierce Brosnan
├─use1
│  └─64X64    <-- Amanda Seyfried 1장
├─use2
│  └─64X64    <-- Andrew Lincoln 1장
├─use3
│  └─64X64
├─use4
│  └─64X64
├─use5
│  └─64X64
└─use6
    └─64X64

### 2. script

>> /ws_python/notebook/machine/cnn_actor/actor.ipynb

```python
# 랜덤시드 고정시키기
np.random.seed(3)

# 1. 데이터 생성하기, ./train 폴더안의 폴더의 수는 classes수에 대응함.
# 픽셀 값이 0 ~ 255는 너무 큼으로 0~1 범위로 변환
train_datagen = ImageDataGenerator(rescale=1./255) 

train_generator = train_datagen.flow_from_directory(
        './train',
        target_size=(64, 64), # 64 x 64 픽셀로 줄임
        batch_size=5,         # 5건씩 처리
        class_mode='categorical')  # 다중 분류

test_datagen = ImageDataGenerator(rescale=1./255)

test_generator = test_datagen.flow_from_directory(
        './test',
        target_size=(64, 64),    
        batch_size=2,
        class_mode='categorical')
```

.....


![VGG](./images/05.png)![VGG](./images/05.png)![VGG](./images/05.png)![VGG](./images/05.png)
num_classes = 5
im_rows = 64
im_cols = 64
in_shape = (im_rows, im_cols, 3)

model = Sequential()
model.add(Conv2D(32, (3, 3), input_shape=in_shape, activation = 'relu'))
model.add(Conv2D(32, (3, 3), activation = 'relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
# model.add(Dropout(0.25))

model.add(Conv2D(32, (3, 3), activation = 'relu'))
model.add(Conv2D(32, (3, 3), activation = 'relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
# model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(128, activation = 'relu'))
model.add(Dropout(0.5))
model.add(Dense(num_classes, activation = 'softmax'))


# 3. 모델 학습과정 설정하기
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# 4. 모델 학습시키기
hist = model.fit_generator(
       train_generator,
       steps_per_epoch=35,# 총 훈련 데이터가 175개이고 배치사이즈가 5임으로 35 step으로 지정
       epochs=30,
       validation_data=test_generator,
       validation_steps=25)  # 총 25개의 검증 샘플이있고 배치사이즈가 1임으로 25로 지정
 
.....

# 총 50개의 검증 샘플이있고 배치사이즈가 2임으로 25로 지정 
scores = model.evaluate_generator(test_generator, steps=25)  
print("%s: %.2f%%" %(model.metrics_names[1], scores[1]*100))
 
.....
 
model.save('actor.h5')
 
.....
 
_temp = np.array([0.1, 0.2, 0.3])
sw = np.argmax(_temp, axis=0)
print('sw:',sw)
 
.....
 
model = load_model('actor.h5')

def display(data):
    # print(data)
    # print(type(data))
    sw= np.argmax(data, axis=0) # 0:열, 1: 행
    # print('sw:', sw)

    if sw == 0:
        sw = 'Amanda Seyfried'
    elif sw == 1:
        sw = 'Andrew Lincoln'
    elif sw == 2:
        sw = 'Anne Hathaway'
    elif sw == 3:
        sw = 'Keira Christina Knightley'        
    elif sw == 4:
        sw = 'Pierce Brosnan'        
        
    return sw    

# 총 50개의 검증 샘플이있고 배치사이즈가 2임으로 25로 지정
output = model.predict_generator(test_generator, steps=25)
# numpy 출력 옵션 변경
np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})
print(test_generator.class_indices) # 클래스명(폴더명) 출력
print(output)
print(type(output))

for item in output:
    print(display(item))    
 
.....
 
# 7. 모델 활용, 데이터 파일은 하위 폴더에 있어야함. /use1/shape 등


use_datagen = ImageDataGenerator(rescale=1./255)
use_generator = use_datagen.flow_from_directory('./use1',target_size=(64, 64), batch_size=1,class_mode='categorical')
output = model.predict_generator(use_generator, steps=1)
print('Amanda Seyfried:', display(output[0]),'\n')

use_generator = use_datagen.flow_from_directory('./use2',target_size=(64, 64), batch_size=1,class_mode='categorical')
output = model.predict_generator(use_generator, steps=1)
print('Andrew Lincoln:',display(output[0]),'\n')

use_generator = use_datagen.flow_from_directory('./use3',target_size=(64, 64), batch_size=1,class_mode='categorical')
output = model.predict_generator(use_generator, steps=1)
print('Anne Hathaway:',display(output[0]),'\n')

use_generator = use_datagen.flow_from_directory('./use4',target_size=(64, 64), batch_size=1,class_mode='categorical')
output = model.predict_generator(use_generator, steps=1)
print('Keira Christina Knightley:',display(output[0]),'\n')
 
use_generator = use_datagen.flow_from_directory('./use5',target_size=(64, 64), batch_size=1,class_mode='categorical')
output = model.predict_generator(use_generator, steps=1)
print('Pierce Brosnan:',display(output[0]),'\n')

