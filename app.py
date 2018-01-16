import io
import os
from PIL import Image
from PIL import ImageOps
import tornado.escape
import tornado.ioloop
import tornado.web
from tornado import gen
import torch
from torchvision import transforms
from torchvision.utils import save_image
from torch.utils.serialization import load_lua
import cStringIO as StringIO

use_cuda = torch.cuda.device_count() > 0

cache  = load_lua( 'model_gan.t7' )
model  = cache.model
immean = cache.mean
imstd  = cache.std
model.evaluate()

BASE_DIR = os.path.dirname(__file__)

@gen.coroutine
def simplify(data):
    w, h  = data.size[0], data.size[1]
    pw    = 8-(w%8) if w%8!=0 else 0
    ph    = 8-(h%8) if h%8!=0 else 0
    data  = ((transforms.ToTensor()(data)-immean)/imstd).unsqueeze(0)
    if pw!=0 or ph!=0:
       data = torch.nn.ReplicationPad2d( (0,pw,0,ph) )( data ).data

    if use_cuda:
       pred = model.cuda().forward( data.cuda() ).float()
    else:
       pred = model.forward( data )

    raise gen.Return(pred[0])

class ApiSimplify(tornado.web.RequestHandler):
  @gen.coroutine
  def post(self):
    requested_file = self.request.files['file'][0]
    fobj = StringIO.StringIO()

    self.set_header("Content-type",  "image/png")
    data = Image.open(io.BytesIO(requested_file['body'])).convert('L')
    data.thumbnail((600, 600))
    data = ImageOps.autocontrast(data)
    img = yield simplify(data)
    pil = transforms.ToPILImage()(img)
    pil.save(fobj, format="png")
    for line in fobj.getvalue():
        self.write(line)

class Index(tornado.web.RequestHandler):
  def get(self):
    self.render('index.html')


application = tornado.web.Application([
  (r"/", Index),
  (r"/api/simplify", ApiSimplify),
],
  template_path=os.path.join(BASE_DIR, 'templates'),
  static_path=os.path.join(BASE_DIR, 'static'),
)

if __name__ == "__main__":
  application.listen(9998)
  tornado.ioloop.IOLoop.instance().start()

