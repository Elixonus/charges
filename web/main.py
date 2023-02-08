from __future__ import annotations
import os
import glob
import random
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from charges import System, PointCharge, FiniteLineCharge
from render import render
from points import Point


plot_ids = []


class PointData(BaseModel):
    x: float
    y: float


class PointChargeData(BaseModel):
    charge: float
    point: PointData


class FiniteLineChargeData(BaseModel):
    charge: float
    point_1: PointData
    point_2: PointData


class ChargesData(BaseModel):
    point_charges: list[PointChargeData]
    finite_line_charges: list[FiniteLineChargeData]


class ViewData(BaseModel):
    min: PointData
    max: PointData


class PlotData(BaseModel):
    charges: ChargesData
    view: ViewData


files = glob.glob("plots/*")

for file in files:
    os.remove(file)

os.rmdir("plots")
os.mkdir("plots")

app = FastAPI()


@app.post("/plots/create")
def plot_create(plot: PlotData):
    plot_id = "P" + "".join(random.choices("0123456789ABCDEF", k=9))
    plot_ids.append(plot_id)

    charges = []

    for point_charge_data in plot.charges.point_charges:
        charge = point_charge_data.charge
        point = Point(point_charge_data.point.x, point_charge_data.point.y)
        point_charge = PointCharge(charge, point)
        charges.append(point_charge)

    for finite_line_charge_data in plot.charges.finite_line_charges:
        charge = finite_line_charge_data.charge
        point_1 = Point(finite_line_charge_data.point_1.x, finite_line_charge_data.point_1.y)
        point_2 = Point(finite_line_charge_data.point_2.x, finite_line_charge_data.point_2.y)
        finite_line_charge = FiniteLineCharge(charge, point_1, point_2, 10)
        charges.append(finite_line_charge)

    system = System(charges)

    try:
        render(plot_id, system, Point(plot.view.min.x, plot.view.min.y), Point(plot.view.max.x, plot.view.max.y),
               "Electric Field and Potential")
    except:
        return {"error": "Could not solve and plot the system."}

    return {"plot_id": plot_id}


@app.get("/plots/view/{plot_id}")
def plot_view(plot_id: str):
    if plot_id in plot_ids:
        return FileResponse(f"plots/{plot_id}.png")
    return "false"


@app.get("/plots/list")
def plot_list():
    return {"plot_ids": plot_ids}
