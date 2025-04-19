-- Copyright (c) 2025, UChicago Argonne, LLC
-- BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
--@ This table includes the locations of internal ports 
--@ that are within the modelled city
--@

CREATE TABLE National_Ports_Locations (
    "national_port"       INTEGER NOT NULL DEFAULT 0, --@ The unique identifier of the port as in the National_Ports table
    "location"            INTEGER NOT NULL DEFAULT 0, --@ The selected location of the internal port (foreign key to the Location table)

    CONSTRAINT nationalportloc_fk FOREIGN KEY (national_port)
    REFERENCES National_Ports (national_port) DEFERRABLE INITIALLY DEFERRED
);