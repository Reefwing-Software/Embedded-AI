<!--
 Copyright (c) 2024 David Such
 
 This software is released under the MIT License.
 https://opensource.org/licenses/MIT
-->

<!-- Linear Regression hypothesis -->
$$
Y = \beta_0 + \beta_1 X
$$

<br>

<!-- Mean Squared Error (MSE) Cost Function in Linear Regression -->
$$
J(\beta) = \frac{1}{m} \sum_{i=1}^{m} \left( h_{\beta}(x^{(i)}) - y^{(i)} \right)^2 
$$

**Where:**

$$
\begin{aligned}
m &\text{ is the number of observations (data points)}, \\
h_{\beta}(x^{(i)}) &\text{ is the predicted value of } y \text{ for the } i\text{-th data point}, \\
y^{(i)} &\text{ is the actual observed value of } y \text{ for the } i\text{-th data point}, \\
\beta &\text{ represents the coefficients (parameters) of the linear regression model}.
\end{aligned}
$$

<!-- Normal Equation used to train Linear Regression -->

$$
\mathbf{\beta} = (\mathbf{X}^T \mathbf{X})^{-1} \mathbf{X}^T \mathbf{y}
$$

$$
\begin{aligned}
&\mathbf{\beta} \quad \text{is the vector of coefficients (parameters) we are solving for.}\\
&\mathbf{X} \quad \text{matrix of input features, each row is an instance and each column is a feature.}\\
&\mathbf{y} \quad \text{is the vector of target values.}\\
&\mathbf{X}^T \quad \text{is the transpose of the matrix } \mathbf{X}.\\
&(\mathbf{X}^T \mathbf{X})^{-1} \quad \text{is the inverse of the matrix product } \mathbf{X}^T \mathbf{X}.
\end{aligned}
$$