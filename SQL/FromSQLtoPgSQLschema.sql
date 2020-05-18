ALTER PROCEDURE Create_Table_Postgres 
	@nombre_origen varchar(100),
	@nombre_destino varchar(100),
	@salida varchar(max) OUTPUT

AS 
BEGIN 
select @salida =  'IF NOT EXISTS (select * from sysobjects where name='''+@nombre_destino+''') create table "' + @nombre_destino + '" (' + o.list + ')' 
--+ CASE WHEN tc.Constraint_Name IS NULL THEN '' ELSE 'ALTER TABLE '  ' ADD CONSTRAINT ' + tc.Constraint_Name  + ' PRIMARY KEY ' + ' (' + LEFT(j.List, Len(j.List)-1) + ')'  END
from    sysobjects so
cross apply
    (SELECT 
        '  "'+column_name+'" ' + 
        data_type + case data_type
            when 'sql_variant' then ''
            when 'text' then ''
            when 'ntext' then ''
            when 'xml' then ''
            when 'decimal' then '(' + cast(numeric_precision as varchar) + ', ' + cast(numeric_scale as varchar) + ')'
            else coalesce('('+case when character_maximum_length = -1 then 'MAX' else cast(character_maximum_length as varchar) end +')','') end + ' ' +
        case when exists ( 
        select id from syscolumns
        where object_name(id)=so.name
        and name=column_name
        and columnproperty(id,name,'IsIdentity') = 1 
        ) then
        'IDENTITY(' + 
        cast(ident_seed(so.name) as varchar) + ',' + 
        cast(ident_incr(so.name) as varchar) + ')'
        else ''
        end + ' ' +
         (case when IS_NULLABLE = 'No' then 'NOT ' else '' end ) + 'NULL '  
          --+ case when information_schema.columns.COLUMN_DEFAULT IS NOT NULL THEN 'DEFAULT '+ information_schema.columns.COLUMN_DEFAULT ELSE '' END + ', ' 
     from information_schema.columns where table_name = so.name
     order by ordinal_position
    FOR XML PATH('')) o (list)
left join
    information_schema.table_constraints tc
on  tc.Table_name       = so.Name
AND tc.Constraint_Type  = 'PRIMARY KEY'
cross apply
    (select '"' + Column_Name + '", '
     FROM   information_schema.key_column_usage kcu
     WHERE  kcu.Constraint_Name = tc.Constraint_Name
     ORDER BY
        ORDINAL_POSITION
     FOR XML PATH('')) j (list)
where   xtype = 'U'
AND name like (@nombre_origen);

SET @salida = (SELECT REPLACE(@salida, 'nvarchar', 'varchar'));
SET @salida = (SELECT REPLACE(@salida, 'datetime', 'timestamp'));
SET @salida = (SELECT REPLACE(@salida, 'uniqueidentifier', 'varchar(100)'));
SET @salida = (SELECT REPLACE(@salida, 'bit', 'boolean'));

END

 