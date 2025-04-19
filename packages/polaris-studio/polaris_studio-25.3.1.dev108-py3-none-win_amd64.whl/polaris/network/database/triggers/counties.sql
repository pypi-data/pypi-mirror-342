-- Copyright (c) 2025, UChicago Argonne, LLC
-- BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
--##
create trigger if not exists counties_populates_geo_enabled_fields_on_new_record after insert on Counties
begin
    update Counties
    set "x" = round(COALESCE(ST_X(ST_Centroid(new.geo)), 0), 8),
        "y" = round(COALESCE(ST_Y(ST_Centroid(new.geo)), 0), 8)
    where Counties.rowid = new.rowid;
end;

--##
create trigger if not exists counties_enforces_x_field_Counties after update of "x" on Counties
begin
    update Counties
    set "x" = round(COALESCE(ST_X(ST_Centroid(new.geo)), new.x), 8)
    where Counties.rowid = new.rowid;
end;

--##
create trigger if not exists counties_enforces_y_field_Counties after update of "y" on Counties
begin
    update Counties
    set "y" = round(COALESCE(ST_Y(ST_Centroid(new.geo)), new.y), 8)
    where Counties.rowid = new.rowid;
end;

--##
create trigger if not exists counties_updates_fields_on_geo_change after update of geo on Counties
begin
        update Counties
    set "x" = round(COALESCE(ST_X(ST_Centroid(new.geo)), old.x), 8),
        "y" = round(COALESCE(ST_Y(ST_Centroid(new.geo)), old.y), 8)
    where Counties.rowid = new.rowid;
end;
