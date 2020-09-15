import json
import os 
import numpy
import csv
import pandas as pd


class JSON2CSV():

    def __init__(self):
        self.img_dict = {}
        self.anno_dict = {}

    def datasetting(self, JsonName, ImagePath):


        # json파일 읽기
        with open(JsonName, 'r') as f:
            json_data = json.load(f)

        # 이미지명 매칭하기
        img_name = os.listdir(ImagePath)

        # json에서 images 값 가져오기
        for images in json_data['images']:

            for name in img_name: 
                
                # json의 filename과 이미지명이 같으면
                if name == images['file_name']:
                    
                    # img_dict에 디텍토리 만들기, id : filename, width, height
                    self.img_dict.setdefault(images['id'] ,[name, images['width'], images['height']])
                
        # json에서 annotations 값 가져오기
        for annotations in json_data['annotations']:

            # segmentation 값 가져오기
            segmt = annotations['segmentation'][0]
            
            # 짝수 번째는 x축
            segmt_x = segmt[::2]

            # 홀수 번째는 y축
            segmt_y = segmt[1::2]

            # x, y, 의 최대, 최소 구하기
            segmt_x_min = int(min(segmt_x))
            segmt_y_min = int(min(segmt_y))
            segmt_x_max = int(max(segmt_x))
            segmt_y_max = int(max(segmt_y))

            # anno_dict에 디렉토리 만들기, id : class, xmin, ymin, xmax, ymax
            self.anno_dict.setdefault(
                annotations['image_id'], [
                    annotations['category_id'], segmt_x_min, segmt_y_min, segmt_x_max, segmt_y_max])

    # CSV 만들기
    def json2csv(self, JsonSaveName):

        # 필드명 지정
        FieldName = [['filename','width','height','class','xmin','ymin','xmax','ymax']]

        # 키, 벨류 나누기 
        for img_id, imagelist in self.img_dict.items():

            # anno_dict와 img_id 매칭이 안될 경우 에외처리
            try: 

                # anno_dict와 img_id 매칭 후 filename, width, height, class, xmin, ymin, xmax, ymax 순으로 append
                FieldName.append(imagelist + self.anno_dict[img_id])
            except:
                True

        # csv 변환 
        ArrayOfData = FieldName
    
        csv.register_dialect(
            'mydialect',
            delimiter = ',',
            quotechar = '"',
            doublequote = True,
            skipinitialspace = True,
            lineterminator = '\r\n',
            quoting = csv.QUOTE_MINIMAL)

        # csv로 저장하기
        with open(JsonSaveName, 'w', newline='', encoding='utf-8') as MycsvFile:
           
            TheDataWriter = csv.writer(MycsvFile, dialect='mydialect')
    
            for row in ArrayOfData:
                TheDataWriter.writerow(row)