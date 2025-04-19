-- Copyright (c) 2025, UChicago Argonne, LLC
-- BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
--@ Join table matching freight shipments and deliveries

CREATE TABLE Shipment_Delivery (
    "shipment"  INTEGER NOT NULL,    --@ Shipment id (foreign key to shipment table)
    "tour"      INTEGER NOT NULL,    --@ Tour id (foreign key to delivery table)
    "leg"       INTEGER NOT NULL,    --@ Leg id in a tour (foreign key to delivery table)

    PRIMARY KEY (shipment, tour, leg)

)