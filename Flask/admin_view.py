from flask import Flask, render_template, Blueprint,
import os
import functools

app = Blueprint('app', __name__)
