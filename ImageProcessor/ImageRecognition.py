import argparse
import base64
import httplib2

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

import WikiParser

with open("../../priv/apiKey.txt") as f:
    api = f.read()
apiVersion = "v1"
DISCOVERY_URL='https://{api}.googleapis.com/$discovery/rest?version={apiVersion}'

labelFeature = 'label'
textFeature = 'text'
faceFeature = 'face'
landmarkFeature = 'landmark'
logoFeature = 'logo'
safeSearchFeature = 'safeSearchFeature'
imageProperties = 'imageProperties'

AvailFeatures = {
    labelFeature:      "LABEL_DETECTION",
    textFeature:       "TEXT_DETECTION",
    faceFeature:       "FACE_DETECTION",
    landmarkFeature:   "LANDMARK_DETECTION",
    logoFeature:       "LOGO_DETECTION",
    safeSearchFeature: "SAFE_SEARCH_DETECTION",
    imageProperties:   "IMAGE_PROPERTIES"
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
                result['label'] = self._entityAnnotation(response['labelAnnotations'])
            if 'textAnnotations' in response:
                result['text'] = self._entityAnnotation(response['textAnnotations'])
            if 'faceAnnotations' in response:
                pass
            if 'landmarkAnnotations' in response:
                result['landmark'] = self._entityAnnotation(response['landmarkAnnotations'])
            if 'logoAnnotations' in response:
                pass
            if 'safeSearchAnnotations' in response:
                pass
            if 'imageProperties' in response:
                pass
            if 'error' in response:
                result = response['error']
                return result

        return responses
        
        
    def _entityAnnotation(self, annotation):
        result = {}
        if 'description' in annotation:
            result['description'] = annotation['description']
        
    
    def _faceAnnotation(self, annotation):
        result = {}
        result['boundingPoly'] = self._boundingPoly(annotation['boundingPoly'])
        result['landmarks'] = map(self._landmark, annotation['landmarks'])
        result['rollAngle'] = annotation['rollAngle']
        result['panAngle'] = annotation['panAngle']
        result['tiltAngle'] = annotation['tiltAngle']
        result['confidence'] = annotation['detectionConfidence']
        result['joy'] = self._likelihood(annotation['joyLikelihood'])
        result['sorrow'] = self._likelihood(annotation['sorrowLikelihood'])
        result['anger'] = self._likelihood(annotation['angerLikelihood'])
        result['surpriseLike']
        
        
    def _likelihood(self, l):
        if l == 'UNKNOWN':
            return -1
        if l == 'VERY_UNLIKELY':
            return 0
        if l == 'UNLIKELY':
            return 1
        if l == 'POSSIBLE':
            return 2
        if l == 'LIKELY':
            return 3
        if l == 'VERY_LIKELY':
            return 4
        
        
    def _boundingPoly(self, poly):
        result = []
        for vertex in poly['vertices']:
            result.append(self._vertex(vertex))
    
        
    def _vertex(self, vertex):
        return (vertex['x'], vertex['y'])
        
        
    def _landmark(self, landmark):
        result = {}
        result['type'] = _type(landmark['type'])
        result['position'] = _position(landmark['position'])
        return result
        
        
    def _position(self, pos):
        return (pos['x'], pos['y'], pos['z'])
        
    
    def _type(self, t):
        return t
        
        
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
    print(i.getResponse(
        # labelFeature,
        # textFeature,
        faceFeature
        # landmarkFeature,
        # logoFeature,
        # safeSearchFeature)
        ))
