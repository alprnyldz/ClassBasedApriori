# ClassBasedApriori

ClassBasedAppriori is an complex association mining algorithm created as ad-hoc development* for the company ELİAR Elektronik San. A.Ş., Automation Solutions for Textile and Glass Batch Industries.

ad-hoc development: creating software without any formal guidelines or processes

## Possible Uses
- It is possible to mine associations in data with univariate and mutivariate classes.
- It is possible to mine associations in continuous data by discretizing it.
- It is possible to mine associations with preselected conditions for root cause analysis.

## Advantages
- ClassBasedApriori scans the dataset only twice thanks to divide and conquer search method, where Apriori scans multiple times using breadth-first search method.
- ClassBasedApriori finds all possible associations and can run an intelligent algorithm on the associations for data mining.
- ClassBasedApriori allows user to draw associations within and between different classes.
- ClassBasedApriori allows user to find associations with certain conditions in a supervised manner.

## Disadvantages
- Since the computational power requirement increases exponentially with the size of the data, it is difficult to work with a large database.
- It processes all necessary or unnecessary information, there is no supervision over the information to be processed.

## Possible Improvements
- On-demand data mining, disabling the brute-force approach
- Apply parallel processing to improve performance
- Interactive plotting to enable exploratory data analysis
- Option to dynamically change support, confidence and lift thresholds while plotting
- Intelligent relative association detection
- Intelligent association filtering

## Presentation


<img width="735" alt="image" src="https://user-images.githubusercontent.com/52410078/141454260-b2207bf1-410c-4cba-888e-a40c0b85d134.png">
<img width="735" alt="image" src="https://user-images.githubusercontent.com/52410078/141455003-153a5f12-91d4-4986-ac4a-ccba07b9771b.png">
<img width="735" alt="image" src="https://user-images.githubusercontent.com/52410078/141454010-54642edb-67d2-4c6b-86bc-c3c8fab080b4.png">
<img width="735" alt="image" src="https://user-images.githubusercontent.com/52410078/141455097-fc327947-1476-4873-9229-0f3d1566d379.png">
<img width="735" alt="image" src="https://user-images.githubusercontent.com/52410078/141454059-c5936752-618f-4730-b767-ec106ca03b3e.png">
