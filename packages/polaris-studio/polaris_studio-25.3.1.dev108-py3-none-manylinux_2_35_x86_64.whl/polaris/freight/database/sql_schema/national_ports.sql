-- Copyright (c) 2025, UChicago Argonne, LLC
-- BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
--@ This table includes the attributes of all ports 
--@ where international shipment goods exit or enter the 
--@ modelled city, including the port name, county,
--@ geographic information, and annual import and export weights
--@

CREATE TABLE National_Ports (
    "national_port"       INTEGER NOT NULL  PRIMARY KEY,  --@ The unique identifier of the port
    "name"                TEXT    NOT NULL,  --@ Name of the port, as commonly known
    "county"              INTEGER NOT NULL DEFAULT 0,  --@ The county FIPS code of the port
    "x"                   NUMERIC NOT NULL DEFAULT 0,  --@ x coordinate of the port. Automatically added by Polaris
    "y"                   NUMERIC NOT NULL DEFAULT 0,  --@ y coordinate of the port. Automatically added by Polaris
    "imports"             NUMERIC NOT NULL DEFAULT 0,  --@ Annual import weights of the port (units: metric tons)
    "exports"             NUMERIC NOT NULL DEFAULT 0  --@ Annual export weights of the port (units: metric tons)
);

SELECT AddGeometryColumn( 'National_Ports', 'geo', SRID_PARAMETER, 'POINT', 'XY', 1);
SELECT CreateSpatialIndex( 'National_Ports' , 'geo' );

CREATE INDEX IF NOT EXISTS "NATIONAL_PORT_I" ON "National_Ports" ("national_port");