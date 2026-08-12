import importlib
packages = ['fastapi','uvicorn','pydantic','pydantic_settings','motor','sklearn','river','paho.mqtt.client','pytest']
for pkg in packages:
    try:
        m = importlib.import_module(pkg)
        print(pkg, getattr(m, '__version__', 'unknown'))
    except Exception as e:
        print(pkg, 'IMPORT_FAIL', repr(e))
