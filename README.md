# tman_automatic_pitch_classification
# JOEY ASHCROFT

## Challenge:
Build a model that automatically predicts the type of baseball pitch being thrown by a right-handed pitcher based on the kinematic measures that describe the flight of the ball acquired from a TrackMan unit. 

## Steps:
### 1. Handle missing values
- This includes finding each row where there are missing values (there were roughly 300 which is a decent ammount)
- If rows had more than 5, delete these rows due to low confidence in measurement accuracy
- If rows just had a couple (mostly spin rate values), interpolate this value using the median grouped by pitcherID/pitchTypeCode


### 2. Data exploration
- Get familiar with data.. specifically the spread of the data in regards to pitches/pitcherID/pitchTypeCode,etc
- Look at the variation from pitch to pitch, as well as from pitcher to pitcher (pretty significantly imbalanced on both accounts)
- These observations are important because they could be potential sources of error to the model later on if significant enough


### 3. Feature engineering
- Manually delete parts of the data we don't need (Euphus pitch/Left handed pitchers/unneeded columns)
- Split the data into train/test set
- Add polynomial and interaction terms of degree 2 (this creates over 209 columns)
- Scale the data using a min_max scaler
- Delete columns with low variance
- Use backward selection method (Recursive Feature Elimination) to delete features that are unimportant (this is an iterative model      execution using feauture selection on Random Forest Classifier)


### 4. Model
- Start with random forest which is a great multiclassification model
- Run the model on the raw cleaned up data to get a baseline to improve upon (94% accuracy)
- Run the model on the optimized polynomial data (94.5% accuracy)
- Tune the hyperparameters and run the model (94.8% accuracy)

- Run other models that are good models for multi-classification (run each model on raw and polynomial data)
1. Decision Trees
2. K Nearest Neighbors (revealed 95.7% accuracy score)
- Tune parameters to increase accuracy (no improvement)
3. Naive Bayes
4. Support Vector Machines


### 5. Evaluate best models (KNN and Random Forest)
- Run models on test data set (scale using scaling coefficients from training set)
- Evaluate not based on accuracy, but on precision/recall/f1-score (this is critical for data sets that are imbalanced)
- Fortunately, the f1-score is very high (>.9 for both models)
- Identify source of error: curveballs and cutters being mistakenly classified as sliders

- Choose model --> KNN model (95% Accuracy/.93 F1-score)




## CONCLUSION:
The KNN model behaves the most accurately and effectively for this multi-classifation problem. The reasons for this are 2 fold because this data is imbalanced in 2 different ways. There is a large imbalance of pitch types and pitches thrown by pitchers. Because of this, I am looking primarily at my classification/confusion matrix while evaluating my model opposed to accuracy.

Because I see a better f1-score for my KNN model (higher accuracy as well), this is my model of choice which I conclude to have a 95% accuracy


### WAYS TO IMPROVE MODEL IF I HAD MORE TIME:
Looking at the confusion matrix/classification report, we can see that the error in large part is due to cutter/curveball misclassifications as sliders. Digging deeper into each model, it is seen that every model has a difficult time distinguishing cutters and sliders.

-> If I had more time, I would take these steps to improve my model:

1. I used a class weighting hyperparameter to account for the class imbalance. Another method would be to try over/under sampling and see how the model responds. I could even oversample the cutters/curveballs more to give the model more efficiency with these pitches
2. Dig deeper into cutters/curveballs and reasons as to why the model would mix them up with sliders
3. Optimize my feature reduction - I set a hard limit of 30 features. If I had more time, I could optimize the number of features to decrease possible overfitting. This optimal number could be much more or much less.
4. I was brainstorming ways to account for the pitcherID imbalance if this became an issue (ended up being ok but could potentially account for some error). One thought is to bin players by speed and build a couple different models depending on player type/parameters. I could also try over/under sampling by pitcherID and see how the model reacts
Overall, I am pleased with the results but also feel this model can be improved upon in terms of the FC/CU/SL classifications






