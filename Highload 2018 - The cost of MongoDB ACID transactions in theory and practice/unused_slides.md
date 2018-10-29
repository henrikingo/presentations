-----
# Write Concern (4.0.2, no-SSL)

| setting | latency (theory) | latency  avg/99 (ms) |
|:--------|-----------------:|---------------------:|
| w:0     | 0                | 0.20 / 0.23          |
| **w:1** | 1 rtt            | 0.61 / 0.66          |
| w:2     | 2 rtt            | 4.12 / 4.93          |
| w:3     | 2 rtt            | 4.08 / 5.33          |
| j:true  | 1 fsync          | 1.25 / 2.05          |
| w:2 j:true     | 2 rtt + 1 fsync | 3.16 / 3.89    |
| w:majority j:false | 2 rtt       | 4.06 / 9.20    |
| w:majority j:true  | 2 rtt + 1 fsync | 3.18 / 4.12|


-----
# Write Concern (Multi-AZ, SSL)

| setting | latency (theory) |       Client1 (ms) | Client2 (ms) |
|:--------|-----------------:|-------------------:|-------------:|
| w:0     | 0                | 0.35 / 0.38        | 0.38 / 0.41  |
| **w:1** | 1 rtt            | 0.99 / 1.13        | 1.38 / 1.61  |
| w:2     | 2 rtt            | 5.14 / 6.40        | 5.13 / 6.24  |
| w:3     | 2 rtt            | 5.23 / 6.63        | 5.00 / 6.17  |
| j:true  | 1 fsync          | 1.83 / 2.92        | 2.01 / 3.02  |
| w:2 j:true     | 2 rtt + 1 fsync | 4.72 / 5.65  | 4.19 / 5.29  |
| w:majority j:false | 2 rtt       | 5.61 / 7.55  | 4.88 / 5.92  |
| w:majority j:true  | 2 rtt + 1 fsync | 4.85 / 5.95 | 4.32 / 5.25 |


-----
# Write Concern (Multi-R, SSL)

| setting | latency (theory) |       Client1 (ms) | Client2 (ms) |
|:--------|-----------------:|-------------------:|-------------:|
| w:0     | 0                | 0.34 / 0.68        | 5.6 / 6.0    |
| **w:1** | 1 rtt            | 1.12 / 1.30        | 72 / 73      |
| w:2     | 2 rtt            | 127 /  173         | 186 / 215    |
| w:3     | 2 rtt            | 140 / 196          | 296 / 299    |
| j:true  | 1 fsync          | 2.16 / 14.9        | 72 / 73      |
| w:2 j:true     | 2 rtt + 1 fsync | 185 / 187    | 214 / 470    |
| w:majority j:false | 2 rtt       | 186 / 192    | 213 / 271    |
| w:majority j:true  | 2 rtt + 1 fsync | 185 / 192| 217 / 480    |
