# Data Collection


## Collecting lease agreement data

```
pdm run process-lease-agreements ./lease_agreements -d 
```

Output will be stored in an SQLite3 database a [`extracted_lease_agreements.db`](../output/extracted_lease_agreements.db)