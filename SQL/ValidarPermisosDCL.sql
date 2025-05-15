
-- Validar permisos DCL en Fabric Lakehouse o Warehouse
WITH
PermisosTotal AS(
	SELECT 
	   CASE WHEN class = 0 THEN DB_NAME()
			 WHEN class = 1 THEN OBJECT_NAME(major_id)
			 WHEN class = 3 THEN SCHEMA_NAME(major_id) END [Securable]
	  , USER_NAME(grantee_principal_id) [User]
	  , *
	FROM sys.database_permissions
),
Columnas AS(
	SELECT object_id, name as column_name, column_id FROM sys.columns
)
SELECT pt.Securable, pt.[User], pt.major_id as table_id, pt.minor_id as column_id, pt.permission_name, pt.state_desc, c.column_name 
FROM PermisosTotal pt
LEFT JOIN Columnas c ON (pt.major_id = c.object_id and pt.minor_id = c.column_id)
WHERE Securable in (SELECT name FROM sys.tables)

-- Validación de a una tabla
-- EXEC sp_table_privileges @table_name = 'dimension_customer';