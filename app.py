# process 로드
import process as pc

# JSON2CSV 클래스 로드
soo = pc.JSON2CSV()

# datasetting(json명, 이미지 경로)
soo.datasetting('coco-1594624682.9582064.json', 'C:/Users/Trip1/Desktop/Faster_RCNN/JSON_CSV_test/200707_emblem')

# 저장할 csv명
soo.json2csv('train_labels_1.csv')