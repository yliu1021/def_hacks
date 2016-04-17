import argparse
import base64
import httplib2

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

api = 'AIzaSyCzLFH3ZdvRoaLSXsp7fSK-NkHBG8kwEUM'
apiVersion = "v1"
DISCOVERY_URL='https://{api}.googleapis.com/$discovery/rest?version={apiVersion}'

AvailFeatures = {
    'label':      "LABEL_DETECTION",
    'text':       "TEXT_DETECTION",
    'face':       "FACE_DETECTION",
    'landmark':   "LANDMARK_DETECTION",
    'logo':       "LOGO_DETECTION",
    'safeSearch': "SAFE_SEARCH_DETECTION",
    'imageProperties':      "IMAGE_PROPERTIES"
}
    
class ImageRecognition():
    
    def __init__(self, imagePath):
        with open(imagePath) as image:
            self.imageData = base64.b64encode(image.read()).decode("UTF-8")
            
        credentials = GoogleCredentials.get_application_default()
        self.service = discovery.build('vision', 'v1', credentials=credentials,
                                  discoveryServiceUrl=DISCOVERY_URL)
    
    
    def getResponse(self, features):
        b = self._createRequest(features)
        request = self.service.images().annotate(body=b)
        response = request.execute()
        return self._parseResponse(response)
        
    
    def _parseResponse(self, responses):
        response['responses']
        for response in responses:
            if response == 'labelannotation':
                response[]
                
        return response
        
        
    def _createRequest(self, features):
        image = {'content': self.imageData}

        f = []
        for feat in features:
            f.append({
                'type': feat,
                'maxResults': 5
            })
        
        r = [{'image': image, 'features': f}]
        b = {'requests': r}
        return b
    
#key AIzaSyCzLFH3ZdvRoaLSXsp7fSK-NkHBG8kwEUM

def getResults(photo_file):
    """Run a label request on a single image"""

    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('vision', 'v1', credentials=credentials,
                              discoveryServiceUrl=DISCOVERY_URL)

    with open(photo_file, 'rb') as image:
        image_content = base64.b64encode(image.read())
        service_request = service.images().annotate(body={
            'requests': [{
                'image': {
                    'content': image_content.decode('UTF-8')
                },
                'features': [{
                    'type': 'LABEL_DETECTION',
                    'maxResults': 5
                }, {
                    'type': 'LANDMARK_DETECTION',
                    'maxResults': 5
                }, {
                    'type': 'IMAGE_PROPERTIES',
                    'maxResults': 5
                }]
            }]
        })
        response = service_request.execute()
        for i in response['responses'][0]['imagePropertiesAnnotation']['dominantColors']['colors']:
            print(i)
        return map(lambda x: (x['description'], x['score']), response['responses'][0]['labelAnnotations'])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('image_file', help='The image you\'d like to label.')
    args = parser.parse_args()
    # print(getResults(args.image_file))
    i = ImageRecognition(args.image_file)
    print(i.getResponse([AvailFeatures['label']]))
    
    #fskdfhdsiufhdskfhdkshf
    
