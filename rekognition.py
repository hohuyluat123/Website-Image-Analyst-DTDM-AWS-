import boto3

aws_access_key_id = "ASIAQYD45YXPM7JBGUPR"
aws_secret_access_key = "5bSgWS8pNYm3WTMgmEpsmNMGWpoqScfJFiclPLXT"
aws_session_token = "FwoGZXIvYXdzEHcaDOhw+BbMVxENPSVi4CLKARbWCiocl38jG2kAJpp3FRQNO1xvPYnQ2SiIcKXFnh3PqlpLKvB++ZBM7w/P+8Va4PPHog94HNLAYxEUiOejEosbhxtlMbpC8KiYxc7GczOGRdUe8Qh5Dvv6ildi6CqfW0k2FoldDs51D8L4ViUkiuRGGI92QdoX0W3Fb3NWiHQMWmhMkfvhElDdVni8x9jBHftScryQdV3wpM72RH8yxvUgogBrmevE4NLlh40lrkCSmxh5eplm+3tkAdaC2WDLsh8aUPx0HjuLzacouKOXjgYyLR+U/BVkymPpztvgrBzmBmhGkaR5s/0iUKht2RfBPIhsMFtuf7TxARhDPeH6lQ=="

def detect_labels(photo, bucket):
    global aws_access_key_id
    global aws_secret_access_key
    global aws_session_token
    client = boto3.client(service_name='rekognition',
                          region_name='us-east-1',
                          aws_access_key_id=aws_access_key_id,
                          aws_secret_access_key=aws_secret_access_key,
                          aws_session_token=aws_session_token)

    response = client.detect_labels(Image={'S3Object': {'Bucket': bucket, 'Name': photo}}, MaxLabels=10)
    mang1 = []
    mang2 = []
    for label in response['Labels']:
        mang1.append('\nLabel: ' + label['Name'])
        mang1.append('\nConfidence: ' + str(label['Confidence']))
        mang1.append('\nInstances:')
        mang = list()
        mang.append(label['Name'])
        mang.append(str(len(label['Instances'])))
        mang2.append(mang)
        for instance in label['Instances']:
            mang1.append('\nBounding box')
            mang1.append('\nTop: ' + str(instance['BoundingBox']['Top']))
            mang1.append('\nLeft: ' + str(instance['BoundingBox']['Left']))
            mang1.append('\nWidth: ' + str(instance['BoundingBox']['Width']))
            mang1.append('\nHeight: ' + str(instance['BoundingBox']['Height']))
            mang1.append('\nConfidence: ' + str(instance['Confidence']))
        for parent in label['Parents']:
            mang1.append("   " + parent['Name'])
    return mang2


def detect_faces(photo, bucket):
    global aws_access_key_id
    global aws_secret_access_key
    global aws_session_token
    client = boto3.client(service_name='rekognition',
                          region_name='us-east-1',
                          aws_access_key_id=aws_access_key_id,
                          aws_secret_access_key=aws_secret_access_key,
                          aws_session_token=aws_session_token)

    response = client.detect_faces(Image={'S3Object': {'Bucket': bucket, 'Name': photo}}, Attributes=['ALL'])
    mang1 = []
    dem = 1
    for faceDetail in response['FaceDetails']:
        mang = list()
        mang.append(str(dem))
        mang.append("from " + str(faceDetail['AgeRange']['Low']) + " to " + str(faceDetail['AgeRange']['High']))

        # Access predictions for individual face details and print them
        mang.append(str(faceDetail['Gender']))
        mang.append(str(faceDetail['Smile']))
        mang.append(str(faceDetail['Eyeglasses']))
        mang.append(str(faceDetail['Emotions'][0]))
        dem = dem + 1
        mang1.append(mang)

    return mang1


def detect_baoho(photo, bucket):
    global aws_access_key_id
    global aws_secret_access_key
    global aws_session_token
    client = boto3.client(service_name='rekognition',
                          region_name='us-east-1',
                          aws_access_key_id=aws_access_key_id,
                          aws_secret_access_key=aws_secret_access_key,
                          aws_session_token=aws_session_token)
    response = client.detect_protective_equipment(Image={'S3Object': {'Bucket': bucket, 'Name': photo}},
                                                  SummarizationAttributes={'MinConfidence': 80,
                                                                           'RequiredEquipmentTypes': ['FACE_COVER',
                                                                                                      'HAND_COVER',
                                                                                                      'HEAD_COVER']})
    responseA = client.detect_faces(Image={'S3Object': {'Bucket': bucket, 'Name': photo}}, Attributes=['ALL'])
    bien = len(responseA['FaceDetails'])
    mang1 = []
    dem = 0
    print('Detected PPE for people in image ' + photo)
    print('\nDetected people\n---------------')
    for person in response['Persons']:
        mang = list()
        mang.append('Person ID' + str(person['Id']))

        print('Body Parts\n----------')
        body_parts = person['BodyParts']
        if len(body_parts) == 0:
            print('No body parts found')
        else:
            for body_part in body_parts:
                print('\t' + body_part['Name'] + '\n\t\tConfidence: ' + str(body_part['Confidence']))
                print('\n\t\tDetected PPE\n\t\t------------')
                ppe_items = body_part['EquipmentDetections']
                if len(ppe_items) == 0:
                    print('\t\tNo PPE detected on ' + body_part['Name'])
                else:
                    dem = dem + 1
                    for ppe_item in ppe_items:
                        print('\t\t' + ppe_item['Type'] + '\n\t\t\tConfidence: ' + str(ppe_item['Confidence']))

                        print('\t\tCovers body part: ' + str(
                            ppe_item['CoversBodyPart']['Value']) + '\n\t\t\tConfidence: ' + str(
                            ppe_item['CoversBodyPart']['Confidence']))
                        print('\t\tBounding Box:')
                        print('\t\t\tTop: ' + str(ppe_item['BoundingBox']['Top']))
                        print('\t\t\tLeft: ' + str(ppe_item['BoundingBox']['Left']))
                        print('\t\t\tWidth: ' + str(ppe_item['BoundingBox']['Width']))
                        print('\t\t\tHeight: ' + str(ppe_item['BoundingBox']['Height']))
                        print('\t\t\tConfidence: ' + str(ppe_item['Confidence']))
            print()
        print()
    mang1.append('Số người mang bảo hộ :' + str(dem))
    print('Person ID Summary\n----------------')
    display_summary('With required equipment', response['Summary']['PersonsWithRequiredEquipment'])
    display_summary('Without required equipment', response['Summary']['PersonsWithoutRequiredEquipment'])
    display_summary('Indeterminate', response['Summary']['PersonsIndeterminate'])
    danhgia = dem / bien
    if danhgia >= 0.9:
        mang1.append('Tỉ lệ không mang bảo hộ: ' + str((1 - danhgia) * 100) + '%')
        mang1.append('Đánh giá: An toàn, đảm bảo tuân thủ quy định')
    elif 0.5 <= danhgia < 0.9:
        mang1.append('Tỉ lệ không mang bảo hộ: ' + str((1 - danhgia) * 100) + '%')
        mang1.append('Đánh giá: Cần tăng cường giám sát, có tình trạng vi phạm an toàn, cần phạt nghiêm')
    else:
        mang1.append('Tỉ lệ không mang bảo hộ: ' + str((1 - danhgia) * 100) + '%')
        mang1.append('Đánh giá: không đảm bảo an toàn, cần mang bảo hộ, yêu cầu thực hiện đúng qui định ')
    print()
    return mang1


# Display summary information for supplied summary.
def display_summary(summary_type, summary):
    print(summary_type + '\n\tIDs: ', end='')
    if len(summary) == 0:
        print('None')
    else:
        for num, id in enumerate(summary, start=0):
            if num == len(summary) - 1:
                print(id)
            else:
                print(str(id) + ', ', end='')
