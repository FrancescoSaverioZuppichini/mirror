# Mirror
## Pytorch CNN Visualisation Tool
*Francesco Saverio Zuppichini*

This is a raw beta so expect lots of things to change and improve over time.

![alt](https://github.com/FrancescoSaverioZuppichini/mirror/blob/master/resources/mirror.gif?raw=true)

An interactive version of this tutorial can be [found here](https://github.com/FrancescoSaverioZuppichini/mirror/blob/master/README.ipynb)

### Getting started

To install mirror run

```
pip install git+https://github.com/FrancescoSaverioZuppichini/mirror.git
```

## Getting Started

A basic example


```python
from mirror import mirror
from mirror.visualisations.web import *
from PIL import Image
from torchvision.models import resnet101, resnet18, vgg16, alexnet
from torchvision.transforms import ToTensor, Resize, Compose

# create a model
model = vgg16(pretrained=True)
# open some images
cat = Image.open("./cat.jpg")
dog_and_cat = Image.open("./dog_and_cat.jpg")
# resize the image and make it a tensor
to_input = Compose([Resize((224, 224)), ToTensor()])
# call mirror with the inputs and the model
mirror([to_input(cat), to_input(dog_and_cat)], model, visualisations=[BackProp, GradCam, DeepDream])
```

    Downloading: "https://download.pytorch.org/models/vgg16-397923af.pth" to /Users/vaevictis/.cache/torch/checkpoints/vgg16-397923af.pth
    100%|██████████| 553433881/553433881 [00:39<00:00, 13900810.38it/s]


     * Serving Flask app "mirror.App" (lazy loading)
     * Environment: production
       WARNING: Do not use the development server in a production environment.
       Use a production WSGI server instead.
     * Debug mode: off


     * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
    127.0.0.1 - - [10/Sep/2019 21:07:03] "GET / HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:03] "GET /static/css/main.fd8c6979.chunk.css HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:03] "GET /static/js/1.2f835df5.chunk.js HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:03] "GET /static/js/main.e85ab74f.chunk.js HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:04] "GET /api/inputs HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:04] "GET /api/model HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:04] "GET /api/visualisation HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:04] "GET /api/model/image/-9223372036580704890/-9223372036580704890/196455791416833112/%3Cbuilt-in%20function%20id%3E/1 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:04] "GET /api/model/image/-9223372036580704890/-9223372036580704890/196439298742416472/%3Cbuilt-in%20function%20id%3E/0 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:04] "GET /manifest.json HTTP/1.1" 404 -
    127.0.0.1 - - [10/Sep/2019 21:07:04] "GET /favicon.ico HTTP/1.1" 404 -
    127.0.0.1 - - [10/Sep/2019 21:07:06] "GET /api/model/layer/output/9223372037162847278?last=0 HTTP/1.1" 500 -
    127.0.0.1 - - [10/Sep/2019 21:07:07] "GET /api/model/layer/output/308065256?last=0 HTTP/1.1" 500 -
    127.0.0.1 - - [10/Sep/2019 21:07:07] "GET /api/model/layer/output/308065263?last=0 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:08] "GET /api/model/image/4425844920/-9223372036546774517/2221084957931467867/308065263/0 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:08] "GET /api/model/image/4425844920/-9223372036546774517/2221105298896581723/308065263/1 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:08] "GET /api/model/image/4425844920/-9223372036546774517/2221130587664020571/308065263/2 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:08] "GET /api/model/image/4425844920/-9223372036546774517/2221135535466345563/308065263/3 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:08] "GET /api/model/image/4425844920/-9223372036546774517/2221140483268670555/308065263/4 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:08] "GET /api/model/image/4425844920/-9223372036546774517/2221144881315181659/308065263/5 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:08] "GET /api/model/image/4425844920/-9223372036546774517/2221151478384948315/308065263/6 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:08] "GET /api/model/image/4425844920/-9223372036546774517/2221156426187273307/308065263/7 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:08] "GET /api/model/image/4425844920/-9223372036546774517/2221160824233784411/308065263/8 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:08] "GET /api/model/image/4425844920/-9223372036546774517/2221167971059364955/308065263/9 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:08] "GET /api/model/image/4425844920/-9223372036546774517/2221172369105876059/308065263/10 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:08] "GET /api/model/image/4425844920/-9223372036546774517/2221176767152387163/308065263/11 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:08] "GET /api/model/image/4425844920/-9223372036546774517/2221186113001223259/308065263/13 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:08] "GET /api/model/image/4425844920/-9223372036546774517/2221181714954712155/308065263/12 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:08] "GET /api/model/image/4425844920/-9223372036546774517/2221191060803548251/308065263/14 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:08] "GET /api/model/image/4425844920/-9223372036546774517/2221196008605873243/308065263/15 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:08] "GET /api/model/image/4425844920/-9223372036546774517/2221199856896570459/308065263/16 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:08] "GET /api/model/image/4425844920/-9223372036546774517/2221204804698895451/308065263/17 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:08] "GET /api/model/image/4425844920/-9223372036546774517/2221209202745406555/308065263/18 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:08] "GET /api/model/image/4425844920/-9223372036546774517/2221214150547731547/308065263/19 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:08] "GET /api/model/image/4425844920/-9223372036546774517/2221218548594242651/308065263/20 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:08] "GET /api/model/image/4425844920/-9223372036546774517/2221222946640753755/308065263/21 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:08] "GET /api/model/image/4425844920/-9223372036546774517/2221227894443078747/308065263/22 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:08] "GET /api/model/image/4425844920/-9223372036546774517/2221232292489589851/308065263/23 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:08] "GET /api/model/image/4425844920/-9223372036546774517/2221237240291914843/308065263/24 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:08] "GET /api/model/image/4425844920/-9223372036546774517/2221241638338425947/308065263/25 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:08] "GET /api/model/image/4425844920/-9223372036546774517/2221248235408192603/308065263/26 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:08] "GET /api/model/image/4425844920/-9223372036546774517/2221253183210517595/308065263/27 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:08] "GET /api/model/image/4425844920/-9223372036546774517/2221266927105864795/308065263/28 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:08] "GET /api/model/image/4425844920/-9223372036546774517/2221276272954700891/308065263/30 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:08] "GET /api/model/image/4425844920/-9223372036546774517/2221271325152375899/308065263/29 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:08] "GET /api/model/image/4425844920/-9223372036546774517/2221280671001211995/308065263/31 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:08] "GET /api/model/image/4425844920/-9223372036546774517/2221285618803536987/308065263/32 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:08] "GET /api/model/image/4425844920/-9223372036546774517/2221290016850048091/308065263/33 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:08] "GET /api/model/image/4425844920/-9223372036546774517/2221294964652373083/308065263/34 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:08] "GET /api/model/image/4425844920/-9223372036546774517/2221298812943070299/308065263/35 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:08] "GET /api/model/image/4425844920/-9223372036546774517/2221303760745395291/308065263/36 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:08] "GET /api/model/image/4425844920/-9223372036546774517/2221308708547720283/308065263/37 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:08] "GET /api/model/image/4425844920/-9223372036546774517/2221313106594231387/308065263/38 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:08] "GET /api/model/image/4425844920/-9223372036546774517/2221318054396556379/308065263/39 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:08] "GET /api/model/image/4425844920/-9223372036546774517/2221321902687253595/308065263/40 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:08] "GET /api/model/image/4425844920/-9223372036546774517/2221326850489578587/308065263/41 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:08] "GET /api/model/image/4425844920/-9223372036546774517/2221331798291903579/308065263/42 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:08] "GET /api/model/image/4425844920/-9223372036546774517/2221338395361670235/308065263/43 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:08] "GET /api/model/image/4425844920/-9223372036546774517/2221343343163995227/308065263/44 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:08] "GET /api/model/image/4425844920/-9223372036546774517/2221347741210506331/308065263/45 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:08] "GET /api/model/image/4425844920/-9223372036546774517/2221352139257017435/308065263/46 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:08] "GET /api/model/image/4425844920/-9223372036546774517/2221357087059342427/308065263/47 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:08] "GET /api/model/image/4425844920/-9223372036546774517/2221361485105853531/308065263/48 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:08] "GET /api/model/image/4425844920/-9223372036546774517/2221366432908178523/308065263/49 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:08] "GET /api/model/image/4425844920/-9223372036546774517/2221370281198875739/308065263/50 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:08] "GET /api/model/image/4425844920/-9223372036546774517/2221375229001200731/308065263/51 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:08] "GET /api/model/image/4425844920/-9223372036546774517/2221380176803525723/308065263/52 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:08] "GET /api/model/image/4425844920/-9223372036546774517/2221384574850036827/308065263/53 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:08] "GET /api/model/image/4425844920/-9223372036546774517/2221389522652361819/308065263/54 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:08] "GET /api/model/image/4425844920/-9223372036546774517/2221393920698872923/308065263/55 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:08] "GET /api/model/image/4425844920/-9223372036546774517/2221398318745384027/308065263/56 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:08] "GET /api/model/image/4425844920/-9223372036546774517/2221409863617475675/308065263/57 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:08] "GET /api/model/image/4425844920/-9223372036546774517/2221417010443056219/308065263/58 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:08] "GET /api/model/image/4425844920/-9223372036546774517/2221423607512822875/308065263/59 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:08] "GET /api/model/image/4425844920/-9223372036546774517/2221430754338403419/308065263/60 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:08] "GET /api/model/image/4425844920/-9223372036546774517/2221435702140728411/308065263/61 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:08] "GET /api/model/image/4425844920/-9223372036546774517/2221440100187239515/308065263/62 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:08] "GET /api/model/image/4425844920/-9223372036546774517/2221444498233750619/308065263/63 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:11] "PUT /api/visualisation HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:12] "GET /api/model/layer/output/308065263?last=0 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:12] "GET /api/model/image/4425844920/-9223372036578155653/1207946015831225440/308065263/0 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:16] "PUT /api/visualisation HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:17] "GET /api/model/layer/output/308065263?last=0 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:17] "GET /api/model/image/4425844920/-9223372036578155653/872664788347909221/308065263/0 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:18] "PUT /api/visualisation HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:19] "GET /api/model/layer/output/308065263?last=0 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:19] "GET /api/model/image/4425844920/-9223372036578155646/2196907796748301415/308065263/0 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:21] "GET /api/model/layer/output/308065256?last=0 HTTP/1.1" 500 -
    127.0.0.1 - - [10/Sep/2019 21:07:22] "GET /api/model/layer/output/308065256?last=0 HTTP/1.1" 500 -
    127.0.0.1 - - [10/Sep/2019 21:07:26] "GET /api/model/layer/output/308071460?last=0 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:26] "GET /api/model/image/4425844920/-9223372036578155646/396973726974342254/308071460/0 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:28] "GET /api/model/layer/output/9223372037162847271?last=0 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:28] "GET /api/model/image/4425844920/-9223372036578155646/2153226398800016496/9223372037162847271/0 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:29] "GET /api/model/layer/output/308071460?last=0 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:29] "GET /api/model/image/4425844920/-9223372036578155646/1375305979229893745/308071460/0 HTTP/1.1" 200 -


    [INFO] cached


    127.0.0.1 - - [10/Sep/2019 21:07:30] "PUT /api/visualisation HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:31] "GET /api/model/layer/output/308071460?last=0 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:31] "GET /api/model/image/4425844920/-9223372036578155646/2174509095623062643/308071460/0 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:32] "PUT /api/visualisation HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:33] "GET /api/model/layer/output/308071460?last=0 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:33] "GET /api/model/image/4425844920/-9223372036578155646/1482006435879974005/308071460/0 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:34] "PUT /api/visualisation HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:34] "PUT /api/visualisation HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:34] "PUT /api/visualisation HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:35] "GET /api/model/layer/output/308071460?last=0 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:35] "GET /api/model/image/4425844920/-9223372036578155653/801744089333101687/308071460/0 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:36] "PUT /api/visualisation HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:36] "GET /api/model/layer/output/308071460?last=0 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:36] "GET /api/model/image/4425844920/-9223372036578155653/651864161792816248/308071460/0 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:36] "PUT /api/visualisation HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:36] "PUT /api/visualisation HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:37] "GET /api/model/layer/output/308071460?last=0 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:37] "GET /api/model/image/4425844920/-9223372036578155653/588070497149252729/308071460/0 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:37] "GET /api/model/layer/output/308071460?last=0 HTTP/1.1" 404 -
    127.0.0.1 - - [10/Sep/2019 21:07:37] "GET /api/model/layer/output/308071460?last=0 HTTP/1.1" 404 -
    127.0.0.1 - - [10/Sep/2019 21:07:37] "PUT /api/visualisation HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:38] "GET /api/model/layer/output/308071460?last=0 HTTP/1.1" 404 -
    127.0.0.1 - - [10/Sep/2019 21:07:38] "GET /api/model/layer/output/308071460?last=0 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:39] "GET /api/model/image/4425844920/-9223372036578155646/2285388246214505594/308071460/0 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:39] "PUT /api/visualisation HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:40] "PUT /api/visualisation HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:40] "GET /api/model/layer/output/308071460?last=0 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:40] "GET /api/model/image/4425844920/-9223372036578155653/1785614581657760892/308071460/0 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:41] "GET /api/model/layer/output/308071460?last=0 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:41] "GET /api/model/image/4425844920/-9223372036578155653/1659425281405351037/308071460/0 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:42] "PUT /api/visualisation HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:43] "GET /api/model/layer/output/308071460?last=0 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:43] "GET /api/model/image/4425844920/-9223372036578155646/964238713778861183/308071460/0 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:43] "PUT /api/visualisation HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:43] "PUT /api/visualisation HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:43] "PUT /api/visualisation HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:44] "GET /api/model/layer/output/308071460?last=0 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:44] "GET /api/model/image/4425844920/-9223372036578155646/1156294807849006208/308071460/0 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:45] "GET /api/model/layer/output/308071460?last=0 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:45] "GET /api/model/layer/output/308071460?last=0 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:45] "GET /api/model/image/4425844920/-9223372036578155646/981595054579119233/308071460/0 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:45] "GET /api/model/image/4425844920/-9223372036578155646/1003154828332364929/308071460/0 HTTP/1.1" 200 -


    [INFO] cached


    127.0.0.1 - - [10/Sep/2019 21:07:45] "PUT /api/visualisation HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:58] "GET /api/model/layer/output/308071460?last=0 HTTP/1.1" 200 -
    127.0.0.1 - - [10/Sep/2019 21:07:58] "GET /api/model/image/4425844920/-9223372036578155639/1631058980920358030/308071460/0 HTTP/1.1" 200 -
    [2019-09-10 21:07:59,017] ERROR in app: Exception on /api/model/layer/output/9223372037162847271 [GET]
    Traceback (most recent call last):
      File "/Users/vaevictis/anaconda3/lib/python3.7/site-packages/flask/app.py", line 2292, in wsgi_app
        response = self.full_dispatch_request()
      File "/Users/vaevictis/anaconda3/lib/python3.7/site-packages/flask/app.py", line 1815, in full_dispatch_request
        rv = self.handle_user_exception(e)
      File "/Users/vaevictis/anaconda3/lib/python3.7/site-packages/flask/app.py", line 1718, in handle_user_exception
        reraise(exc_type, exc_value, tb)
      File "/Users/vaevictis/anaconda3/lib/python3.7/site-packages/flask/_compat.py", line 35, in reraise
        raise value
      File "/Users/vaevictis/anaconda3/lib/python3.7/site-packages/flask/app.py", line 1813, in full_dispatch_request
        rv = self.dispatch_request()
      File "/Users/vaevictis/anaconda3/lib/python3.7/site-packages/flask/app.py", line 1799, in dispatch_request
        return self.view_functions[rule.endpoint](**req.view_args)
      File "/Users/vaevictis/Documents/mirror/mirror/App.py", line 112, in api_model_layer_output
        layer_cache[layer] = self.current_vis(input_clone, layer)
      File "/Users/vaevictis/Documents/mirror/mirror/visualisations/web/WebInterface.py", line 14, in __call__
        return self.callable(input_image, layer, **self.call_params)
      File "/Users/vaevictis/Documents/mirror/mirror/visualisations/core/DeepDream.py", line 86, in __call__
        scale=scale)
      File "/Users/vaevictis/Documents/mirror/mirror/visualisations/core/DeepDream.py", line 67, in deep_dream
        from_down = self.deep_dream(image_down, n - 1, top, scale)
      File "/Users/vaevictis/Documents/mirror/mirror/visualisations/core/DeepDream.py", line 67, in deep_dream
        from_down = self.deep_dream(image_down, n - 1, top, scale)
      File "/Users/vaevictis/Documents/mirror/mirror/visualisations/core/DeepDream.py", line 67, in deep_dream
        from_down = self.deep_dream(image_down, n - 1, top, scale)
      [Previous line repeated 1 more time]
      File "/Users/vaevictis/Documents/mirror/mirror/visualisations/core/DeepDream.py", line 77, in deep_dream
        return self.step(image, steps=8, save=top == n + 1)
      File "/Users/vaevictis/Documents/mirror/mirror/visualisations/core/DeepDream.py", line 45, in step
        dreamed = self.image_var.data.squeeze(0)
    AttributeError: 'DeepDream' object has no attribute 'image_var'
    127.0.0.1 - - [10/Sep/2019 21:07:59] "GET /api/model/layer/output/9223372037162847271?last=0 HTTP/1.1" 500 -


It will automatic open a new tab in your browser

![alt](https://github.com/FrancescoSaverioZuppichini/mirror/blob/master/resources/mirror.png?raw=true)

On the left you can see your model tree structure, by clicking on one layer all his children are showed. On the right there are the visualisation settings. You can select your input by clicking on the bottom tab.

![alt](https://raw.githubusercontent.com/FrancescoSaverioZuppichini/mirror/master/resources/inputs.png)


## Available Visualisations
All visualisation available for the web app are inside `.mirror.visualisations.web`.
### Weights
![alt](https://github.com/FrancescoSaverioZuppichini/mirror/blob/master/resources/weights.png?raw=true)
### Deep Dream
![alt](https://github.com/FrancescoSaverioZuppichini/mirror/blob/master/resources/deepdream.png?raw=true)
### Back Prop / Guide Back Prop
By clicking on the radio button 'guide', all the relus negative output will be set to zero producing a nicer looking image
![alt](https://github.com/FrancescoSaverioZuppichini/mirror/blob/master/resources/backprop.png?raw=true)
## Grad Cam / Guide Grad Cam
![alt](https://github.com/FrancescoSaverioZuppichini/mirror/blob/master/resources/grad_cam.png?raw=true)

### Using with Tensors
If you want, you can use the vanilla version of each visualisation by importing them from  `.mirror.visualisation.core`. 


```python
from mirror.visualisations.core import GradCam

# create a model
model = vgg16(pretrained=True)
# open some images
cat = Image.open("./cat.jpg")
dog_and_cat = Image.open("./dog_and_cat.jpg")
# resize the image and make it a tensor
to_input = Compose([Resize((224, 224)), ToTensor()])

cam = GradCam(model, device='cpu')
cam(to_input(cat).unsqueeze(0), None) # will return the output image and some additional information
```

## Create a Visualisation
To create a visualisation you first have to subclass the `Visualisation` class and override the`__call__` method to return an image and, if needed, additional informations. The following example creates a custom visualisation that just repeat the input `repeat` times. So


```python
from mirror.visualisations.core import Visualisation

class RepeatInput(Visualisation):

    def __call__(self, inputs, layer, repeat=1):
        return inputs.repeat(repeat, 1, 1, 1), None

```

This class repeats the input for `repeat` times.
### Connect to the web interface
To connect our fancy visualisation to the web interface, we have to create a `WebInterface`. Easily, we can use `WebInterface.from_visualisation` to generate the communication channel between our visualisation and the web app. 

It follows and example


```python
from mirror.visualisations.web import WebInterface
from functools import partial

params = {'repeat' : {
                     'type' : 'slider',
                     'min' : 1,
                     'max' : 100,
                     'value' : 2,
                     'step': 1,
                     'params': {}
                 }
        }


visualisation = partial(WebInterface.from_visualisation, RepeatInput, params=params, name='Repeat')
```


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-1-274e90ff3655> in <module>
         13 
         14 
    ---> 15 visualisation = partial(WebInterface.from_visualisation, RepeatInput, params=params, name='Repeat')
    

    NameError: name 'RepeatInput' is not defined


First we import `WebInterface` and `partial`. Then, we create a dictionary where each **they key is the visualisation parameter name**. In our example, `RepeatInput` takes a parameter called `repeat`, thus we have to define a dictionary `{ 'repeat' : { ... }' }`. 

The value of that dictionary is the configuration for one of the basic UI elements: *slider*, *textfield* and *radio*. 

The input is stored in the `value` slot.

Then we call `WebInterface.from_visualisation` by passing the visualisation, the params and the name. We need to wrap this function using `partial` since `mirror` will need to dynamically pass some others parameters, the current layer and the input, at run time.

![alt](https://github.com/FrancescoSaverioZuppichini/mirror/blob/master/resources/repeat_slider.jpg?raw=true)
The final result is 

![alt](https://github.com/FrancescoSaverioZuppichini/mirror/blob/master/resources/repeat_example.jpg?raw=true)


![alt](https://github.com/FrancescoSaverioZuppichini/mirror/blob/master/resources/dummy.jpg?raw=true)


## Change the front-end
All the front-end is developed usin [React](https://reactjs.org/) and [Material-UI](https://material-ui.com/), two very known frameworks, making easier for anybody to contribuite.

You can customise the front-end by changing the source code in `mirror/client`. After that, you need to build the react app and move the file to the server static folder.

**I was not able to serve the static file directly from the /mirror/client/build folder** if you know how to do it any pull request is welcome :)

```
cd ./mirror/mirror/client // assuming the root folder is called mirror
npm run build
```
Then you need to move the fiels from the `mirror/mirror/client/build` folder to `mirror/mirror`. You can remove all the files in `mirror/mirro/static`
```
mv ./build/static ../ && cp ./build/* ../static/
```

### TODO
- [x] Cache reused layer 
- [x] Make a generic abstraction of a visualisation in order to add more features  
- [x] Add dropdown as parameter
- [x] Add text field
- [x] Support multiple inputs
- [x] Support multiple models
- Add all visualisation present here https://github.com/utkuozbulak/pytorch-cnn-visualizations
    * [x] [Gradient visualization with vanilla backpropagation](#gradient-visualization)
    * [x] [Gradient visualization with guided backpropagation](#gradient-visualization) [1]
    * [x] [Gradient visualization with saliency maps](#gradient-visualization) [4]
    * [x] [CNN filter visualization](#convolutional-neural-network-filter-visualization) [9]
    * [x] [Deep dream](#deep-dream) [10]
    * [ ] [Class specific image generation](#class-specific-image-generation) [4]
    * [x] [Grad Cam](https://arxiv.org/abs/1610.02391)

- [ ] Add a `output_transformation` params for each visualisation to allow better customisation 
- [ ] Add a `input_transformation` params for each visualisation to allow better customisation 
