
#!/usr/bin/env python3
# -*- coding: UTF-8 -*-


from ..api import MdbAPI



app = MdbAPI("metricdb.db")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

