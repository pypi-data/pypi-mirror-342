-- Copyright (c) 2025, UChicago Argonne, LLC
-- BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
--##
create trigger if not exists national_ports_populates_geo_enabled_fields_on_new_record after insert on National_Ports
begin
    update National_Ports
    set "x" = round(COALESCE(ST_X(new.geo), 0), 8),
        "y" = round(COALESCE(ST_Y(new.geo), 0), 8)
    where National_Ports.rowid = new.rowid;
end;

--##
create trigger if not exists national_ports_enforces_x_field_National_Portss after update of "x" on National_Ports
begin
    update National_Ports
    set "x" = round(COALESCE(ST_X(new.geo), new.x), 8)
    where National_Ports.rowid = new.rowid;
end;

--##
create trigger if not exists national_ports_enforces_y_field_National_Portss after update of "y" on National_Ports
begin
    update National_Ports
    set "y" = round(COALESCE(ST_Y(new.geo), new.y), 8)
    where National_Ports.rowid = new.rowid;
end;

--##
create trigger if not exists national_ports_updates_fields_on_geo_change after update of geo on National_Ports
begin
        update National_Ports
    set "x" = round(COALESCE(ST_X(new.geo), old.x), 8),
        "y" = round(COALESCE(ST_Y(new.geo), old.y), 8)
    where National_Ports.rowid = new.rowid;
end;
