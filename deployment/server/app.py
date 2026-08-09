import base64
import io
import time
from contextlib import asynccontextmanager
import numpy as np
from fastapi import FastAPI, File, HTTPException, UploadFile. Request
from PIL import Image
from inference import Predictor