import torch

# تحميل النموذج
model = torch.hub.load("ultralytics/yolov5:v7.0", "yolov5s")

# حفظ النموذج
torch.save(model.state_dict(), "yolov5.pt")  # حفظ النموذج باسم yolov5.pt على جهازك
