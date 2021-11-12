# ClassBasedApriori

Apriori is an algorithm for frequent item set mining and association rule learning over relational databases. Apriori uses breadth-first search method.
ClassBasedAppriori is an complex ad-hoc developed association mining algorithm for specific use. ClassBasedAppriori uses divide and conquer search method.

Possible Uses
It is possible to use on data with univariate and mutivariate classes.
It is possible to run the algorithm by discretizing the continuous data. (much more efficient and less power consuming than apriori)
Using classes as input variables allows the user to explore associations in a controlled manner.
It is possible to find associations with conditions for root cause analysis.

Advantages
ClassBasedApriori scans the dataset only twice thanks to divide and conquer search method, where Apriori scans multiple times.
ClassBasedApriori finds all possible associations and can run an intelligent algorithm on the associations for data mining.
ClassBasedApriori allows the user to draw associations within and between different classes.
ClassBasedApriori allows the user to find associations with certain conditions.

Disadvantages
Since the computational power requirement increases exponentially with the size of the data, it is difficult to work with a large database.
It processes all necessary or unnecessary information, there is no supervision over the information to be processed.

Possible Improvements
On-demand data mining, disabling the brute-force approach
Apply parallel processing to improve performance
Interactive plotting to enable exploratory data analysis
  Option to dynamically change support, confidence and lift thresholds while plotting
Intelligent relative association detection
Intelligent association filtering

<img width="838" alt="image" src="https://user-images.githubusercontent.com/52410078/141449033-f6e78cef-9150-4c45-be0c-f73d22dcfb52.png">

<img width="824" alt="image" src="https://user-images.githubusercontent.com/52410078/141450610-f0acab2a-cb08-486a-a799-22511821ceca.png">
<img width="766" alt="image" src="https://user-images.githubusercontent.com/52410078/141451336-d9d1d939-64dd-4b6f-ba46-6d7b9a9be197.png">
<img width="766" alt="image" src="https://user-images.githubusercontent.com/52410078/141451617-be0624ad-d780-4cdb-bc4d-c9b1b790ed07.png">
<img width="766" alt="image" src="https://user-images.githubusercontent.com/52410078/141452120-d8e1aeb1-615a-4f73-9a98-076b7fd1338d.png">
