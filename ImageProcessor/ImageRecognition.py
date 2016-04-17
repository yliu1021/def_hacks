import argparse
import base64
import httplib2

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

import WikiParser

with file("../priv/apiKey.txt") as f:
    api = f.read()
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
    
    
    def getResponse(self, *f):
        features = []
        for feature in f:
            if feature in AvailFeatures:
                features.append(AvailFeatures[feature])
        b = self._createRequest(features)
        request = self.service.images().annotate(body=b)
        response = request.execute()
        return self._parseResponse(response)
        # return response
        
    
    def _parseResponse(self, responses):
        result = {}
        for response in responses:
            if 'labelAnnotations' in response:
                labels = response['labelAnnotations']
                for label in labels:
                    if 'description' in label:
                        pass

        return responses

        
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

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('image_file', help='The image you\'d like to label.')
    args = parser.parse_args()
    # print(getResults(args.image_file))
    i = ImageRecognition(args.image_file)
    print(i.getResponse('label', 'text', 'face', 'landmark', 'logo'))

