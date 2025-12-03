Para ejecutar el programa correctamente, asegúrate de cumplir con los siguientes requisitos:

1. Tener instalado SQL Server en tu máquina (puede ser SQL Server Express).

2. Contar con la base de datos `PruebaDB`. Se anexa junto al programa un archivo de respaldo (.bak) o script SQL para crearla.

3. Tener instalado el **ODBC Driver 17 for SQL Server**.  
   - Para comprobarlo, abre PowerShell y ejecuta:  
     Get-OdbcDriver | Where-Object Name -like "*SQL Server*"  
   - Si aparece "ODBC Driver 17 for SQL Server" en la lista, ya está listo yey!! 

4. Al crear la base de datos, asegúrate de que tu usuario de Windows tenga permisos de conexión (se usa `Trusted_Connection=yes`).

![alt text](image-1.png)

NOTA:  
Si no tienes instalado el ODBC Driver 17, puedes descargarlo desde este link:
https://learn.microsoft.com/es-mx/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver17  
O desde tu navegador de confianza: Microsoft ODBC Driver for SQL Server


![alt text](image-2.png)