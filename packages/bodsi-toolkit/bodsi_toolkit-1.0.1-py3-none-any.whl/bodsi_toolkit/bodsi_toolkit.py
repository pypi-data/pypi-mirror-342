"""
The Bi-Objective Dynamic Systems Identification (BODSI_TOOLKIT) toolkit contains
the necessary functions to identify dynamic systems based on Polynomial NARX models,
where two objective functions are simultaneously addressed: (i) minimization of
dynamic error and (ii) static curve fitting, resulting in a
Pareto-Optimal Set of Candidate Models.

In this context, generating the Pareto-Optimal Set is framed as a p-lambda problem,
where J(Parameters) = lambda * Ed + (1 - lambda) * Ee, i.e., the linear combination
of dynamic (Ed) and static (Ee) errors.

As this is a regulation problem, if the detected polynomial structure is suitable
for the dynamic data and capable of representing the system's static behavior,
the bi-objective estimator will generate non-biased parameters [1].

The BODSI_TOOLKIT class has the following associated functions (methods):
    1 – generateCandidateTerms: generates the set of candidate terms for
     a polynomial NARX model.

    2 – sortByERR: sorts the set of candidate terms by the Error Reduction
     Ratio criterion.
    
    3 – AkaikeInformationCriterion: aids in deciding the number of candidate
     terms to consider by applying the Akaike Information Criterion.
    
    4 – getClusters: builds the clusters of terms present in the candidate
     model and makes them available as a cluster matrix.
    
    5 – buildRegressorMatrix: constructs the regressor matrix based on the
     candidate model.
    
    6 – buildStaticMatrix: builds the clustered matrix representing the
     static model, assuming y(k) = y(k-1) = y(k-2) = ...
                            u(k) = u(k-1) = u(k-2) = ...
    
    7 – buildMapping: builds the mapping matrix between the estimated
     parameters of the bi-objective estimator and their corresponding cluster coefficients.
    
    8 – generateParetoSet: generates the Pareto-Optimal Set for the detected
     structure using the p-lambda technique, with the cost functions being
     the dynamic and static errors of the identified model.
    
    9 – correlationDecisionMaker: a decision-maker based on the correlation
     between the dynamic error and the model's validation data. If the
     structure is adequate, the minimal correlation ensures that the estimated
     parameters are, on average, equal to the real parameters of the discretized system.
    
    10 – getInfo(Model): auxiliary function to retrieve some details of
     interest from the model.
    
    11 – simulateModel: simulates the identified model for dynamic validation
     input and initial conditions provided by the user.
    
    12 – buildStaticModel: builds a matrix containing the clusters of terms
     and their respective coefficients.
    
    13 – displayStaticModel: simulates the static model for a static input
     and displays the result on a panel. Note: this function should only be
     used if the model lacks input term clusters with a non-linearity degree of 2 or higher.
    
    14 – displayModel: constructs a matrix decoding the identified model and
     writing it in the form of ys and us with their respective delays and parameters.
    
    15 – rmse: auxiliary function calculating the Root Mean Square Error,
     useful for dynamic validation of the identified model.
    
    16 – correla: auxiliary function calculating the cross-correlation coefficient
     between two signals; it can validate the identified static model.
    
    17 – combinationWithRepetition: auxiliary function that produces combinations
     with repetition of n elements taken m at a time. It generates all possible
     combinations of candidate terms based on user-defined input/output delays
     and non-linearity degree.
    
    18 – delay: auxiliary function generating a delay in a signal. Used to delay
     input and output data, i.e., y(k-delay), u(k-delay).
    
    19 – removeClusters: aims to extract spurious clusters from the candidate
     model based on static function analysis.
    
    20 - checkSubarrayForGNLY: Check if there is nonlinearity in y
    
    21 - correlationFunction: auxiliary function to show a Correlation Function
     of a signal ou vector
    
    22 - buildStaticResponse: auxiliary Function that builds the static matrix
     of a model when the degree of non-linearity in y is greater than or equal to 2.
    
    23 - buildStaticModelAgroup: auxiliary Function that builds the static
    modelo when the degree of non-linearity in y is greater than or equa
    to 2.
    
    For more information, use help BODSI_TOOLKIT in the command prompt.
     To access the functions, use "function name", e.g.:
    >> help('getInfo')
    
    
[1] Márcio F.S. Barroso, Ricardo H.C. Takahashi, Luis A. Aguirre,
 Multi-objective parameter estimation via minimal correlation criterion,
 Journal of Process Control, Volume 17, Issue 4, 2007, Pages 321-332,
 ISSN 0959-1524. https://doi.org/10.1016/j.jprocont.2006.10.005.

Bi-Objective Dynamic Systems Identification Package
Márcio F. S. Barroso, Universidade Federal de São João del-Rei (UFSJ)
Eduardo M. A. M. Mendes, Universidade Federal de Minas Gerais (UFMG)
Jim Jones S. Marciano, Computer Scientist.
March 2025.
"""
from inspect import signature
from numpy import (array, prod, sort, max, any, zeros_like, round, ones, mean, 
                   dot, sqrt, ndarray, floor, sum, zeros, roll, unique, hstack, 
                   newaxis, where, log, argmin, var, ones_like, linspace, isinf,
                   isnan, bincount, column_stack)
from numpy.linalg import pinv, inv, LinAlgError
from itertools import combinations_with_replacement
from matplotlib.pyplot import (figure, plot, axhline, title, xlabel, text,
                             ylabel, legend, grid, box, show, subplots, axis)
#==============================================================================
def generateCandidateTerms(nonlinearityDegree, delays):
    """
    The function [model, Tterms, type] = generateCandidateTerms(nonlinearityDegree, delays) is part of the
    Bi-Objective System Identification Package for polynomial models. Its purpose is to
    generate candidate terms for process and noise with a degree of nonlinearity
    and maximum delays provided by the user. The output is the combination of all
    terms as a function of delays and nonlinearity degree, as follows:

    Inputs:
        nonlinearityDegree ==> degree of nonlinearity: if equal to zero, it indicates
                                that the model is linear, and its static representation
                                is of the type Y = AX; if the value is greater than or equal
                                to 1, it indicates that the model is nonlinear and its static
                                representation is of the type Y^nonlinearityDegree = AX^nonlinearityDegree + BX^(nonlinearityDegree-1) + ... M,
                                where M is a constant.

        delays ==> a vector of dimension between 1 and 3 containing the maximum
                   delays for input, output, and noise. If the vector has a
                   dimension of 1, it indicates that the model is of type AR,
                   linear or nonlinear depending on nonlinearityDegree; if the vector has a
                   dimension of 2, it indicates that the model is ARX, linear or
                   nonlinear depending on nonlinearityDegree;

    Outputs:
        model ==> a coded representation of the structure containing
                  candidate terms where the number of columns corresponds
                  to the degree of nonlinearity. The regressors are coded as:
                  y(k-i) = 100i --> output terms
                  u(k-j) = 200j --> input terms
                  The model will be the combination of all possible terms.
      Tterms ==> Total Nuber of Terms
        type ==> reveals the representation type, i.e., (AR, ARX,
                 NAR, NARX, polynomial).
    """
    #Verify the dimensions of the inputs and outputs of the function
    nargin = signature(generateCandidateTerms).parameters
    if len(nargin) != 2:
        raise ValueError("The function requires 2 inputs")
    #Check if the nonlinearityDegree is a positive integer
    test = nonlinearityDegree % 1
    if test != 0 or nonlinearityDegree < 0 :
        raise("The degree of nonlinearity must be a positive integer")
    #Check if the delays vector is not empty. Delays must have
    #a dimension greater than or equal to 1 and less than 4.    
    # Check if the 'delays' list is empty
    if not delays:  # Checks if 'delays' is empty
        raise ValueError("The 'delays' variable must have a dimension greater than or equal to 1")
    delays = array(delays)
    #--------------------------------------------------------------------------
    #Test if the values inside the delays vector are positive integers and if 
    #the dimension is less than or equal to 3
    #--------------------------------------------------------------------------
    # Tests
    test2 = prod(delays % 1)  # Test if all elements are integers
    test3 = prod(delays)      # Test if the product of delays is positive
    test4 = test3 % 1            # Test if the product is an integer
    # Check conditions
    if test2 != 0 or test3 <= 0 or test4 != 0 or delays.ndim > 1 or len(delays) > 2:
        raise ValueError("Delays must be positive integers and the dimension must be less than or equal to 2")
    # --------------------------------------------------------------------------
    # Build the candidate terms matrix.
    # Case 1 - build an AR model
    # --------------------------------------------------------------------------
    if len(delays) == 1 and nonlinearityDegree == 0:
        lagy = delays[0]
        linear = [[i] for i in range(1001, 1000 + lagy + 1)]
        model = linear
        typmodel = 'Polynomial AR'
    
    # --------------------------------------------------------------------------
    # Case 2 - build an ARX model
    # --------------------------------------------------------------------------
    elif len(delays) == 2 and nonlinearityDegree == 0:
        lagy = delays[0]
        lagu = delays[1]
        linear = [[i] for i in range(1001, 1000 + lagy + 1)] + \
                 [[i] for i in range(2000, 2000 + lagu + 1)]
        model = linear
        typmodel = 'Polynomial ARX'
    
    # --------------------------------------------------------------------------
    # Case 3 - build a NAR model
    # --------------------------------------------------------------------------
    elif len(delays) == 1 and nonlinearityDegree != 0:
        lagy = delays[0]
        linear = [[0]] + [[i] for i in range(1001, 1000 + lagy + 1)]
        model = combinationWithRepetition(linear, nonlinearityDegree)
        typmodel = 'Polynomial NAR'
    
    # --------------------------------------------------------------------------
    # Case 4 - build a NARX model
    # --------------------------------------------------------------------------
    elif len(delays) == 2 and nonlinearityDegree != 0:
        lagy = delays[0]
        lagu = delays[1]
        linear = [[0]] + [[i] for i in range(1001, 1000 + lagy + 1)] + \
                 [[i] for i in range(2001, 2000 + lagu + 1)]
        model = combinationWithRepetition(linear, nonlinearityDegree)
        typmodel = 'Polynomial NARX'
    
    # --------------------------------------------------------------------------
    # Check if the dimension of the delays vector is compatible with the number of
    # required inputs
    # --------------------------------------------------------------------------
    elif len(delays) > 2:
        raise ValueError('The delays variable has a maximum dimension of 2')

   
    # Reorder rows such that 0 always appears last in the row
    model = array([
        sort(row)[::-1] if 0 in row else row for row in model
    ])  


    # --------------------------------------------------------------------------
    # Calculate the number of terms in the model
    # --------------------------------------------------------------------------
    Tterms = len(model)
    # --------------------------------------------------------------------------
    
    return model, Tterms, typmodel
#=====================================================================================================

#==============================================================================
def sortByERR(model, ui, yi):
    """
    The function [model, ERR] = sortByERR(model, ui, yi)
    is part of the Bi-objective Dynamic Systems Identification package for
    Polynomial Models. Its purpose is to detect the candidate structure that
    best explains the output data, as follows:
    
    Input:
           model ==> coded representation of the structure containing candidate
                     terms where the number of columns corresponds to the degree
                     of nonlinearity, and the rows represent the regressors, coded as:
                                            y(k-i) = 100i --> output terms
                                            u(k-j) = 200j --> input terms
              ui ==> input identification vector to be used for parameter estimation
                     of the coded structure
              yi ==> output identification vector to be used for parameter estimation
                     of the coded structure
    
    
    Output:
    
          model ==> Model with detected structure containing both process and
                    noise terms
            ERR ==> Error Reduction Rate of the model
    """
    
        
    # Construir matriz de regressores para o modelo completo com erro
    P = buildRegressorMatrix(model, ui, yi)

    # Parâmetros do modelo de processo e ruído
    Parameters = pinv(P) @ yi
    
    if len(Parameters) != 0:
                # Erros normalizados
        ERR = zeros((len(Parameters), 1))

    
        for i in range(len(Parameters)):
            ERR[i, 0] = (Parameters[i]**2 * (P[:, i].T @ P[:, i])) / (yi.T @ yi)
    
        # Ordenar erros do modelo de processo
        ERR, I = zip(*sorted(zip(ERR.flatten(), range(len(ERR))), reverse=True))
        ERR = array(ERR).reshape(-1, 1)
        model = model[I, :]

    
    return model, ERR
#==============================================================================

#==============================================================================
def AkaikeInformationCriterion(model, ui, yi):
    """
    The function [f,mint] = Akaike Information Criterion(model, ui, yi)
     is part of the Bi-Objective System Identification Package for Polynomial Models.
     Its purpose is to estimate the number of model terms by Akaike
     Information Criterion, as follows:
    
     Input:
           model ==> coded representation of the structure containing candidate
                     terms where the number of columns corresponds to the degree
                     of nonlinearity, and the rows represent the regressors, coded as:
                                            y(k-i) = 100i --> output terms
                                            u(k-j) = 200j --> input terms
              ui ==> input identification vector to be used for parameter estimation
                     of the coded structure
              yi ==> output identification vector to be used for parameter estimation
                     of the coded structure
     Output:
    
          f ==> Akaike function vector
       mint ==> minimal process terms by Akaike criterion
    """
    
    #Calculate AIC
    #--------------------------------------------------------------------------
    P = buildRegressorMatrix(model, ui, yi)
    Par = pinv(P) @ yi
    N = len(ui)
    f = zeros(len(Par))
    for i in range(len(Par)):
        linha = P[:,:i+1] 
        yhat = linha @ Par[:i+1]
        r = var(yi-yhat)
        f[i] = N * log(r) + 2*(i+1)        
    # Passo 5: Encontrar o índice de f que tem o valor mínimo
    mint = argmin(f)+1
    
    return f, mint
#==============================================================================

#==============================================================================
def getClusters(Model):
    """
    The function getClusters(Model) obtains the clusters (grouping of terms) from the model.

    Parameters:
        Model: Coded representation of the structure containing candidate terms, 
               where the number of columns corresponds to the degree of nonlinearity. 
               Regressors are coded as:
               y(k-i) = 100i --> output terms
               u(k-j) = 200j --> input terms

    Returns:
        clusters: Matrix containing the composition of clusters (grouping of terms) 
                  present in the dynamic model.
    """
    if Model is None:
        raise ValueError('The function requires one input.')

    # Extract clusters from the Model
    clusters = floor(Model / 1000).astype(int)

    # Find unique clusters (rows) and discard additional outputs
    clusters = unique(clusters, axis=0)

    return clusters
#==============================================================================

#==============================================================================
def buildRegressorMatrix(model, ui, yi):
    """
    The function buildRegressorMatrix(model, ui, yi) is part of the System
    Identification Package for polynomial models. Its purpose is to construct
    the regressors' matrix of candidate terms, as follows:
    
    Input:
        model ==> coded representation of the structure containing candidate
                  terms where the number of columns corresponds to the degree
                  of nonlinearity, and the rows represent the regressors, coded as:
                                     y(k-i) = 100i --> output terms
                                     u(k-j) = 200j --> input terms

        ui ==> input identification vector to be used for parameter estimation
              of the coded structure
        yi ==> output identification vector to be used for parameter estimation
              of the coded structure
              
    Output:
        P ==> Regressors Matrix of Process terms
    """
    # Verify the number of inputs and outputs of the function
    if ui is None or yi is None:
        raise ValueError('The function requires at least 3 input variables')

    # Evaluate if there is a noise model to build the regressors matrix appropriately
    lengths = [len(ui), len(yi)]
    if len(set(lengths)) != 1:
        raise ValueError('The input and output vectors must have the same length')

    # Verify the dimensions of the input and output vectors
    if len(ui) != len(yi):
        raise ValueError('The input and output vectors must have the same length')

    # Adjust dimensions
    ui = array(ui).reshape(-1, 1)
    yi = array(yi).reshape(-1, 1)
   

    # Initialize the delay and type matrices
    delayMatrix = zeros_like(model)
    typeMatrix = zeros_like(model)

    # Conditions for updating the matrices
    cond1 = (model > 0) & (model < 2000)
    cond2 = (model >= 2000)

    # Update matrices based on conditions
    delayMatrix[cond1] = model[cond1] - 1000
    typeMatrix[cond1] = round(model[cond1] / 1000)
    delayMatrix[cond2] = model[cond2] - 2000
    typeMatrix[cond2] = round(model[cond2] / 1000)

    # Initialize necessary variables
    rows, cols = model.shape
    Paux = ones((len(ui), cols))
    P = ones((len(ui), rows))

    # Build the Process and Noise regressors matrix
    for i in range(rows):
        for j in range(cols):
            if typeMatrix[i, j] == 0:
                Paux[:, j] = ones(len(ui))
            elif typeMatrix[i, j] == 1:
                Paux[:, j] = delay(yi, delayMatrix[i, j]).flatten()
            elif typeMatrix[i, j] == 2:
                Paux[:, j] = delay(ui, delayMatrix[i, j]).flatten()
            P[:, i] = prod(Paux, axis=1)

    return P
#==============================================================================

#==============================================================================
def buildStaticMatrix(clusters, u, y):
    """
    The function buildStaticMatrix(clusters, u, y) builds the static "regressors" matrix.

    Parameters:
        clusters: Matrix containing the grouping of terms and their coefficients.
        u: Static input data.
        y: Output data.

    Returns:
        Pest: Static data matrix.
    """
    # Verify the dimension of inputs
    if clusters is None or u is None or y is None:
        raise ValueError('The function requires 3 inputs.')

    # Verify the compatibility of the dimensions of the input and output vectors
    #--------------------------------------------------------------------------
    u = array(u)
    y = array(y)
    if u.ndim == 1:
        u = u[:, newaxis]
    if y.ndim == 1:
        y = y[:, newaxis]
       
    if u.shape[0] != y.shape[0]:
        raise ValueError('The vectors must have the same dimension')

    # Initialize variables
    rows, cols = clusters.shape
    value = zeros((len(u), cols))
    Pest = zeros((len(u), rows))

    # Build the static matrix
    if cols == 1:
        linear1 = clusters == 0
        # Check if the model is linear
        if not linear1[0]:
            Pest = hstack((ones_like(u), u))
        else:  # Non-linear case
            for i in range(rows):
                for j in range(cols):
                    if clusters[i, j] == 0:
                        value[:, j] = ones_like(u).flatten()
                    elif clusters[i, j] == 1:
                        value[:, j] = y.flatten()
                    elif clusters[i, j] == 2:
                        value[:, j] = u.flatten()
                Pest[:, i] = prod(value, axis=1)
    else:
        for i in range(rows):
            for j in range(cols):
                if clusters[i, j] == 0:
                    value[:, j] = ones_like(u).flatten()
                elif clusters[i, j] == 1:
                    value[:, j] = y.flatten()
                elif clusters[i, j] == 2:
                    value[:, j] = u.flatten()
            Pest[:, i] = prod(value, axis=1)

    return Pest
#==============================================================================

#==============================================================================
def buildMapping(Model):
    """
    The function buildMapping(Model) obtains the matrix that maps the dynamic 
    parameters to the equivalent grouping coefficients.

    Parameters:
        Model: Coded representation of candidate terms structure, where the number of columns 
               corresponds to the degree of nonlinearity. Regressors are coded as:
               y(k-i) = 100i --> output terms
               u(k-j) = 200j --> input terms

    Returns:
        A: Matrix that maps the dynamic parameters to the equivalent grouping coefficients.
    """
    if Model is None:
        raise ValueError('The function requires one input.')

    # Extract clusters from the Model
    clusters = floor(Model / 1000).astype(int)

    # Find unique clusters and their positions
    unique_clusters, idx = unique(clusters, axis=0, return_inverse=True)

    # Initialize the mapping matrix
    num_clusters = unique_clusters.shape[0]
    A = zeros((num_clusters, Model.shape[0]), dtype=int)

    for i in range(num_clusters):
        rows = (idx == i)
        A[i, rows] = 1

    return A
#==============================================================================

#==============================================================================
def generateParetoSet(P, E, A, yi, y, N, flag=0):
    """
    The function generateParetoSet(P, E, A, yi, y, N, flag) Constructs the 
    Pareto-Optimal Set for a bi-objective parameter estimator.

    Parameters:
        P: Process regressor matrix for a Polynomial NARX representation.
        E: "Static regressors" matrix for the same representation.
        A: Mapping matrix between dynamic parameters and grouping coefficients.
        yi: Process output data used for identification.
        y: Steady-state output data used for identification.
        N: Number of elements in the Pareto-Optimal Set.
        flag: If 1, shows the Optimal-Pareto set.

    Returns:
        PARAMETERS: Set of all estimated parameters for Pareto candidate models.
        VAL: Objective function values for each Pareto point.
    """
    if P is None or E is None or A is None or yi is None or y is None:
        raise ValueError('The function requires at least 6 inputs...')

    # Adjust dimensions

    # Verify the compatibility of the dimensions of the input and output vectors
    #--------------------------------------------------------------------------
    y = array(y)
    yi = array(yi)
    if y.ndim == 1:
        y = y[:, newaxis]
    if yi.ndim == 1:
        yi = yi[:, newaxis]
    

    # Generate weight values for the convex combination
    lambdas = linspace(0, 1, N)

    # Initialize variables
    PARAMETERS = []
    VAL = []

    # Generate Pareto-Optimal
    for lam in lambdas:
        B = lam * P.T @ P + (1 - lam) * ((E @ A).T @ (E @ A))
        try:
            B_inv = inv(B)
        except LinAlgError:
            continue

        parameter = B_inv @ (lam * P.T @ yi + (1 - lam) * (E @ A).T @ y)

        if not any(isinf(parameter)) and not any(isnan(parameter)):
            dynamic_error = ((yi - P @ parameter).T @ (yi - P @ parameter)).item()
            static_error = ((y - E @ A @ parameter).T @ (y - E @ A @ parameter)).item()
            PARAMETERS.append(parameter.flatten())
            VAL.append([dynamic_error, static_error])

    PARAMETERS = array(PARAMETERS).T
    VAL = array(VAL)

    if flag == 1:
        figure()
        plot(VAL[:, 0], VAL[:, 1], 'b')
        title('Optimal-Pareto Set')
        xlabel('Dynamic Error')
        ylabel('Static Error')
        plot(VAL[:, 0], VAL[:, 1], 'r*')
        grid(True)
        show()

    return PARAMETERS, VAL
#==============================================================================

#==============================================================================
def correlationDecisionMaker(model, PARAMETERS, uv, yv):
    """
    The function correlationDecisionMaker(model, PARAMETERS, uv, yv) Implements 
    the "correlation decision-maker" (CD) for selecting the "best" model among 
    the Pareto-optimal set (Candidate Models).

    Parameters:
        model: Encoded matrix containing the structure of the model.
        PARAMETERS: Matrix containing the estimated parameters for the Candidate Models.
        uv: Input data (validation).
        yv: Output data (validation).
       

    Returns:
        parametros: Set (vector) of parameters chosen by the correlation decision-maker.
        correl: Value of the correlation returned by the decision-maker.
        p: Pareto point chosen by the decision-maker.
        r: Vector of calculated correlations.
    """
    if model is None or PARAMETERS is None or uv is None or yv is None:
        raise ValueError("The function requires four inputs.")

    # Ensure proper dimensions of input and output vectors
    #uv = array(uv)
    #yv = array(yv)
    #if yv.ndim == 1:
    #    yv = yv[:, newaxis]
    #if uv.ndim == 1:
    #    uv = uv[:, newaxis]

    # Initialize variables
    l , c = PARAMETERS.shape
    r = 1000*ones(c)  # Initialize correlation array with high values

    # Simulation and evaluation of each Pareto-optimal set point
    for k in range(c):
        _, lag, _, _ = getInfo(model)  # Get model information
        if not isinf(PARAMETERS[:, k]).any():  # Skip invalid parameter sets
            Y = simulateModel(model, PARAMETERS[:, k], uv, yv[:lag])  # Simulate mode
            if max(Y) < 3 * max(yv):  # Ensure simulated output is within reasonable bounds
                r[k] = correla((yv - Y), Y)  # Calculate correlation
            else:
                r[k] = 1000# Penalize outliers
    # Decision based on minimum correlation
    correl = min(r)
    p = argmin(r)
    parametros = PARAMETERS[:, p]

    return parametros, correl, p, r
#==============================================================================

#==============================================================================
def getInfo(model):
    """
    The function getInfo(model) is part of the Bi-Objective System Identification 
    Package for polynomial models. Its     purpose is to retrieve relevant 
    information in the Bi-Objective System Identification process, such as 
    Process terms, Noise terms, maximum delays, etc., as follows:

    Input:
          model ==> coded representation of the structure containing candidate
                    terms where the number of columns corresponds to the degree
                    of nonlinearity. The regressors are coded as follows:
                    y(k-i) = 100i --> output terms
                    u(k-j) = 200j --> input terms

    Outputs:
          numProcessTerms ==> number of process terms
          maxDelay ==> maximum delay present in the model
          maxOutputDelay ==> maximum delay of output terms
          maxInputDelay ==> maximum delay of input terms

    """

    # Verify the input of the function
    if model is None:
        raise ValueError("The function requires one input only")

        
    numProcessTerms = len(model)

    
    # Get models in y
    Jy = (model > 0) & (model < 2000)
    maxOutputDelay = max(model[Jy] - 1000)

    # Get models in u
    Ju = (model >= 2000)
    maxInputDelay = max(model[Ju] - 2000)


    # Get the maximum delay
    maxDelay = max([maxOutputDelay, maxInputDelay])


    return numProcessTerms, maxDelay, maxOutputDelay, maxInputDelay
#==============================================================================

#==============================================================================
def simulateModel(model, Parameters, uv, y0):
    """
    Simulates the identified model.

    Parameters:
        model: Encoded representation of the structure containing candidate terms.
               The number of columns corresponds to the degree of nonlinearity.
               Regressors are coded as:
               y(k-i) = 100i --> output terms
               u(k-j) = 200j --> input terms.
        Parameters: Vector of parameters estimated by the ELS.
        uv: Input data (time-discrete).
        y0: Output initial condition.
        

    Returns:
        yhat: Simulated output (infinite steps ahead, free simulation).
    """
    if model is None or Parameters is None or uv is None or y0 is None:
        raise ValueError('The function requires 4 inputs.')

    # Ensure the proper dimensions of the input and output vectors
    # Ensure proper dimensions of input and output vectors
    uv = array(uv)
    
    if uv.ndim == 1:
        uv = uv[:, newaxis]

    # Get model information and maximum delay
    _, max_delay, _, _ = getInfo(model)
    if len(y0) != max_delay:
        raise ValueError(f'y0 must be a {max_delay} x 1 matrix.')

    # Generate initial conditions
    rows, cols = model.shape
    l = len(uv)
    #signal = zeros(rows)

    # Initialize yhat and set initial conditions
    yhat = zeros(l)
    yhat[:max_delay] = y0.flatten()
    type_code = floor(model / 1000).astype(int)
    delay = (model - (type_code * 1000)).astype(int)
    k1 = where(type_code == 1)  # Output terms
    k2 = where(type_code == 2)  # Input terms
    
    # Build the simulation
    P = ones(type_code.shape)
    for i in range(max_delay, l):
        P[k1] = yhat[i - delay[k1]]  
        P[k2] = uv[i - delay[k2]].T
        
        yhat[i] = dot(prod(P, axis=1), Parameters)

    return yhat
#==============================================================================

#==============================================================================
def buildStaticModel(Model, Parameters):
    """
    The function [staticModel] = buildStaticModel(Model, Parameters)
    is part of the Bi-Objective Bi-Objective System Identification Package for Polynomial Models.
    Its purpose is to obtain the clusters (grouping of terms) and their respective
    grouping coefficients, as follows:
    
    Inputs:
        Model ==> coded representation of the structure containing candidate
                  terms where the number of columns corresponds to the degree
                  of nonlinearity. The regressors are coded as follows:
                  y(k-i) = 100i --> output terms
                  u(k-j) = 200j --> input terms
    Parameters ==> vector of process parameters estimated
    
    Outputs:
      staticModel ==> matrix containing the information for assembling the
                      static model, where columns from 1 to end-1 represent the
                      code of the term grouping, such as:
                      0 = constant, 1 = output, 2 = input. The number of columns
                      corresponds to the degree of nonlinearity, as follows (example):
                      [0, 0, c] ==> constant term grouping, with the last column
                                    being the coefficient's value
                      [1, 1, c] ==> cross-term grouping with a degree of
                                    nonlinearity 2, with the last column being the coefficient's value
    
    """
    
    # Verify the dimensions of the input and output of the function
    if len([Model, Parameters]) != 2:
        raise ValueError("The function requires two inputs")
    
    # Extract clusters from the Model
    clusters = floor(Model / 1000).astype(int)
    
    # Find unique clusters and their positions
    unique_clusters, idx = unique(clusters, axis=0, return_inverse=True)
    
    # Sum parameters for each unique cluster and calculate their coefficients
    coefficients = bincount(idx, weights=Parameters)
    
    # A possible static model, by cluster and coefficients
    staticModel = column_stack((unique_clusters, coefficients))
    
    return staticModel
#==============================================================================

#==============================================================================
def displayStaticModel(staticModel, u, y, p):
    """
    The function displayStaticModel(staticModel, p) is part of the System
    Identification Package for polynomial models. Its purpose is to display the
    static model in string format, allowing the user to visualize the encoded model
    in terms of input and output data, as follows:
    
    Inputs:
    staticModel ==> matrix model containing the grouping of terms and their
                    respective grouping coefficients
              u ==> static input vector
              y ==> static output vector
              p ==> presents the equation on a panel.
    
    Outputs:
       eqest ==> vector containing the equation in string format
        yest ==> vector of calculated output
    
    """

    # Verify the dimension of the input and output of the function
    #--------------------------------------------------------------------------
    if staticModel is None or u is None or y is None or p is None:
        raise ValueError("The function requires four inputs")

    # Chamar a função checkSubarrayForGNLY com staticModel
    result = checkSubarrayForGNLY(staticModel)
    
    # Verificar o resultado
    if result == 1:
        eqest = buildStaticModelAgroup(staticModel)
        yest, _, _ = buildStaticResponse(staticModel, u, y)
        if p == 1:
            eqestLatex = f"{eqest}"
            figure(figsize=(6, 2))
            text(0.5, 0.5, eqestLatex, fontsize=16, ha='center', va='center')
            title("Static Equation", pad=20)
            axis("off")
            show()
            
            print(' ')
            print('Static Model: ')
            print(eqest)
    else:
        # Initialize the denominator and numerator matrices
        #--------------------------------------------------------------------------
        denominator = []
        numerator = []
    
        # Initialize strings for numerator and denominator equations
        #--------------------------------------------------------------------------
        numeratorEquation = ''
        denominatorEquation = ''
    
        # Iterate over each row of the staticModel matrix
        #--------------------------------------------------------------------------
        for i in range(staticModel.shape[0]):
            # Initialize the row equation as an empty string
            #----------------------------------------------------------------------
            equation = ''
    
            # Iterate over each column, except the last (parameter)
            #----------------------------------------------------------------------
            for j in range(staticModel.shape[1] - 1):
                value = staticModel[i, j]
                if value == 1:
                    term = 'y'
                elif value == 2:
                    term = 'u'
                else:
                    term = ''  # Ignore the constant term (0)
    
                #------------------------------------------------------------------
                # Concatenate the term in the equation, ignoring constant terms
                #------------------------------------------------------------------
                if term:
                    if not equation:
                        equation = term
                    else:
                        equation += ' * ' + term
    
            # Multiply the equation by the corresponding parameter
            #----------------------------------------------------------------------
            parameter = staticModel[i, -1]
            if not equation:
                equation = f"{parameter:+.4f}"
            else:
                equation = f"{parameter:+.4f} * {equation}"
    
            # Check if the row should be added to the numerator or denominator
            #----------------------------------------------------------------------
            if 1 in staticModel[i, :]:
                denominator.append(staticModel[i, :])
                # Invert the parameter sign and add
                invertedParameter = -parameter
                if not denominatorEquation:
                    if 2 in staticModel[i, :]:
                        denominatorEquation = f"{invertedParameter:+.4f} * u"
                    else:
                        denominatorEquation = f"{invertedParameter:+.4f}"
                else:
                    if 2 in staticModel[i, :]:
                        denominatorEquation += f"  {invertedParameter:+.4f} * u"
                    else:
                        denominatorEquation += f"  {invertedParameter:+.4f}"
            else:
                numerator.append(staticModel[i, :])
                if not numeratorEquation:
                    numeratorEquation = equation
                else:
                    numeratorEquation += f"  {equation}"
    
        # Remove the initial '+' sign, if present, in the numerator
        #--------------------------------------------------------------------------
        if numeratorEquation.startswith('+'):
            numeratorEquation = numeratorEquation[1:]
    
        # Build the final equation
        #--------------------------------------------------------------------------
        eqest = f"y = ({numeratorEquation}) / (1 {denominatorEquation})"
    
        # Evaluate the calculated output
        #--------------------------------------------------------------------------
        Y = eval(f"({numeratorEquation}) / (1 {denominatorEquation})")
        yest = array(Y)
    
        # Display the equation in a panel if p == 1
        #--------------------------------------------------------------------------
        if p == 1:
            eqestLatex = f"$y = \\frac{{{numeratorEquation}}}{{1 {denominatorEquation}}}$"
            figure(figsize=(6, 2))
            text(0.5, 0.5, eqestLatex, fontsize=16, ha='center', va='center')
            title("Static Equation", pad=20)
            axis("off")
            show()
            
            print(' ')
            print('Static Model: ')
            print(eqest)

    return yest.reshape(-1,1), eqest
#==============================================================================

#==============================================================================
def displayModel(model, parameters, p):
    """
    The function displayModel(model, parameters, p) is part of the System
    Identification Package for polynomial models. Its purpose is to create a vector
    containing the elements of the model in string format, allowing the user to
    visualize the encoded model in terms of input, output, and noise data, when applicable, as follows:
    
    Inputs:
          model ==> coded representation of the structure containing candidate
                    terms where the number of columns corresponds to the degree
                    of nonlinearity. The regressors are coded as follows:
                    y(k-i) = 100i --> output terms
                    u(k-j) = 200j --> input terms
                    e(k-l) = 300l --> noise terms
    
     parameters ==> parameters estimated by the least squares estimator based on
                    the structure of the model and identification data
    
                p ==> presents the equation on a panel.
    
    Outputs:
               eq ==> vector containing the equation in string format, where each
                    row corresponds to a regressor and its parameter.
    
    """
    
    # Verify the dimension of the input and output of the function
    #--------------------------------------------------------------------------
    if model is None or parameters is None or p is None:
        raise ValueError('The function requires three inputs')
    
    # Initialize an empty string list
    #--------------------------------------------------------------------------
    eq = [''] * (model.shape[0] + 1)
    
    # Add "y(k) =" in the first row
    #--------------------------------------------------------------------------
    eq[0] = 'y(k) ='
    
    # Iterate through the rows of the model
    #--------------------------------------------------------------------------
    for i in range(model.shape[0]):
        # Initialize the term as empty
        #----------------------------------------------------------------------
        term = ''
        # Iterate through the columns of the model
        #----------------------------------------------------------------------
        for j in range(model.shape[1]):
            # Get the value of the model at the current position
            #------------------------------------------------------------------
            value = model[i, j]
            # Define the appropriate term based on the value
            #------------------------------------------------------------------
            if value >= 1000 and value < 2000:
                single_term = f'y(k-{value - 1000})'
            elif value >= 2000 and value < 3000:
                single_term = f'u(k-{value - 2000})'
            elif value >= 3000:
                single_term = f'e(k-{value - 3000})'
            else:
                single_term = ''
            #------------------------------------------------------------------
            # Multiply the elements of the columns
            #------------------------------------------------------------------
            if single_term:
                if not term:
                    term = single_term
                else:
                    term = f'{term}*{single_term}'
        
        # Add the corresponding parameter
        #----------------------------------------------------------------------
        if parameters[i] < 0:
            if not term:
                term = f'  {parameters[i]:+.4f}'
            else:
                term = f'  {parameters[i]:+.4f}*{term}'
        else:
            if not term:
                term = f' + {parameters[i]:+.4f}'
            else:
                term = f' + {parameters[i]:+.4f}*{term}'
        
        # Remove the first space and the addition sign if present
        #----------------------------------------------------------------------
        if term.startswith(' + '):
            term = term[3:]
        elif term.startswith(' - '):
            term = f'-{term[3:]}'
        
        # Add the term to the string list
        #----------------------------------------------------------------------
        eq[i + 1] = term
        
        formatted_result = [eq[0]]
        for line in eq[1:]:
            # Remover colchetes e espaços adicionais
            formatted_line = line.strip().replace('[', '').replace(']', '')
            formatted_result.append(formatted_line)
        eq = formatted_result
    if p == 1:
        # Convert the string list into a single string
        #------------------------------------------------------------------
        fullText = '\n'.join(eq)
        
        # Create a new figure with a specified size
        #------------------------------------------------------------------
        fig, ax = subplots(figsize=(5, 4))
        axis('off')
        title('Identified Model')
        
        # Add an edit control with sliders
        #------------------------------------------------------------------
        text(0.5, 0.5, fullText, fontsize=10, ha='left', va='center')
        
        show()
        
        print(' ')
        print('Dynamic Model:')
        for item in eq:
            print(f' {item}')
            
    return eq
#==============================================================================

#=====================================================================================================
def rmse(x, y):
    """
    The function rmse(x, y) is part of the Bi-Objective System Identification Package
    for polynomial models, aimed at calculating the RMSE - Root Mean Square Error, as follows:
    
    Inputs:
                x ==> base vector for the RMSE calculation
                y ==> vector for comparison and RMSE calculation relative to x
    Outputs:
                r ==> RMSE value calculated between x and y

    """

    # Ajustar as dimensões das variáveis de entrada
    # --------------------------------------------------------------------------
    if len(x.shape) > 1 and x.shape[1] > x.shape[0]:
        x = x.T
    if len(y.shape) > 1 and y.shape[1] > y.shape[0]:
        y = y.T
    
    if x.shape != y.shape:
        raise ValueError('The vectors must have the same dimensions')
    
    # --------------------------------------------------------------------------
    # Definir o erro de ajuste
    # --------------------------------------------------------------------------
    e = (x - y)
    em = (x - mean(y))
    
    # --------------------------------------------------------------------------
    # Definir o erro quadrático
    # --------------------------------------------------------------------------
    errorE = dot(e.T, e)
    errorM = dot(em.T, em)
    
    # --------------------------------------------------------------------------
    # Calcular o valor do RMSE
    # --------------------------------------------------------------------------
    r = (sqrt(errorE)) / (sqrt(errorM))
    
    return r
#=================================================================================

#=================================================================================
def correla(X, Y):
    """
    The function correla(X, Y) calculates the cross-correlation coefficient 
    between two vectors.

    Parameters:
        X: Vector or signal (n x 1).
        Y: Vector or signal (n x 1).

    Returns:
        rho: Cross-correlation coefficient between X and Y.
    """
    if X is None or Y is None:
        raise ValueError("The function requires two inputs.")

    # Ensure X and Y are column vectors
    X = array(X)
    Y = array(Y)
    
    if X.ndim == 1:
        X = X[:, newaxis]
    if Y.ndim == 1:
        Y = Y[:, newaxis]

    if X.shape[0] != Y.shape[0]:
        raise ValueError("X and Y must have the same length.")

    # Calculate numerator and denominator of the correlation coefficient
    num = sum(X * Y) - (len(X) * mean(X) * mean(Y))
    den = sqrt((sum(X * X) - len(X) * (mean(X)**2)) *
                  (sum(Y * Y) - len(Y) * (mean(Y)**2)))

    # Calculate and return the correlation coefficient
    rho = num / den
    return rho
#=================================================================================

#=====================================================================================================
def combinationWithRepetition(v, d):
    """
    The function combinationWithRepetition(v, d) is part of the Estimation of Dynamic
    Systems package for discrete polynomial models. It calculates the combination
    of the elements of vector v given the dimension d, as follows:

    Inputs:
        v ==> vector of elements to be combined, with repetition
        d ==> dimension of the combinations

    Outputs:
        combinations ==> combinations where the number of columns is the dimension
                         of the combinations

    """

    # Verify the dimensions of the inputs and outputs of the function
    # --------------------------------------------------------------------------
    if not isinstance(v, (list, ndarray)):
        raise TypeError('The first input must be a list or numpy array')
    if not isinstance(d, int):
        raise TypeError('Dimension must be a positive integer')
    if d <= 0:
        raise ValueError('Dimension must be a positive integer')
    # --------------------------------------------------------------------------

    # Verify the dimension of the vector to be combined
    # --------------------------------------------------------------------------
    v = array(v).flatten()  # Ensure v is a one-dimensional array
    # --------------------------------------------------------------------------

    # Name the dimension
    # --------------------------------------------------------------------------
    k = d
    # --------------------------------------------------------------------------

    # Perform the combination with repetition
    # --------------------------------------------------------------------------
    if k == 1:
        combinations = v[:, None]
    else:
        combinations = array(list(combinations_with_replacement(v, k)))
    # --------------------------------------------------------------------------

    return combinations
#=====================================================================================================

#==============================================================================
def delay(signal, delay):
    """
    The function delay(signal, delay) is part of the Bi-Objective System Identification
    Package for polynomial models. Its purpose is to apply a pure time delay to a signal, as follows:
    
    Inputs:
        signal ==> vector to be shifted in time
         delay ==> delay to be applied to the signal
        
    Outputs:
        delayedSignal ==> vector shifted by a delay in discrete time
        
    """
    
    # Adjust the input and output characteristics of the delay function
    # --------------------------------------------------------------------------
    if signal is None or delay is None:
        raise ValueError('2 inputs are required: signal and delay')
    # --------------------------------------------------------------------------
    
    # Convert signal to a NumPy array if it is not already
    signal = array(signal).reshape(-1, 1)
    # Verify the dimension of the signal vector. If the number of columns is greater than
    # the number of rows, the vector is transposed.
    # --------------------------------------------------------------------------
    rows, cols = signal.shape if signal.ndim == 2 else (len(signal), 1)
    if cols > rows:
        signal = signal.T
    # --------------------------------------------------------------------------
    
    # Delay the signal vector
    # --------------------------------------------------------------------------
    if delay == len(signal):
        delay = delay - 1
    
    delayedSignal = zeros_like(signal)
    if delay != 0:
        delayedSignal[delay:] = signal[:-delay]
    else:
        delayedSignal = signal
    # --------------------------------------------------------------------------

    return delayedSignal
#==============================================================================

#==============================================================================
def removeClusters(model, cy, cu):
    """
    The function removeClusters(model, cy, cu) is part of the System
    Identification Package for polynomial models. Its purpose is to remove
    clusters from the model as specified by the user, as follows:
    
    Inputs:
        model ==> coded representation of the structure containing candidate
                  terms where the number of columns corresponds to the degree
                  of nonlinearity. The regressors are coded as follows:
                  y(k-i) = 100i --> output terms
                  u(k-j) = 200j --> input terms
                  e(k-l) = 300l --> noise terms
                  The model will include the combination of all possible terms.
                  
        cy    ==> cluster (Grouping of Terms) of output terms to be removed
                  from the candidate model, corresponding to the degree of
                  nonlinearity of the grouping.
        cu    ==> cluster (Grouping of Terms) of input terms to be removed
                  from the candidate model, corresponding to the degree of
                  nonlinearity of the grouping.
                  
    Outputs:
        model ==> new set of candidate terms without the presence of the
                  clusters cy and cu.
                  
    """
    
    # --------------------------------------------------------------------------
    if len([model, cy, cu]) != 3:
        raise ValueError('The function requires 3 inputs')
    
    # --------------------------------------------------------------------------
    # Extract clusters: create a vector with all clusters, the size of the model
    # --------------------------------------------------------------------------
    clusters = floor(model / 1000).astype(int)
    
    # --------------------------------------------------------------------------
    # Candidates to be excluded
    # --------------------------------------------------------------------------
    exclude = (sum(clusters == 1, axis=1) == cy) & (sum(clusters == 2, axis=1) == cu)
    
    # --------------------------------------------------------------------------
    # Filter the model by removing the indicated clusters
    # --------------------------------------------------------------------------
    model = model[~exclude, :]
    
    # --------------------------------------------------------------------------
    # Verify if the term grouping exists
    # --------------------------------------------------------------------------
    if model.size == 0:
        raise ValueError('The indicated grouping does not exist in the model.')
    
    return model
#==============================================================================

#=====================================================================================================
def checkSubarrayForGNLY(matrix):
    """
    The function checkSubarrayForGNLY(matrix) is part of the System
    Identification Package for polynomial models. checkSubarrayForGNLY checks 
    if there is a row with subarray [1 1] in any column combinations
    
    Inputs:
        matrix ==> The input matrix to be checked.
    
    Outputs:
        result ==> Returns 1 if there is at least one row with subarray [1 1], else returns 0.
    
    """
    
    # Initialize the result to 0 (not found)
    result = 0
    
    # Get the number of rows and columns in the matrix
    numRows, numCols = matrix.shape
    
    # Iterate over each row of the matrix
    for i in range(numRows):
        # Iterate over each combination of two columns
        for j in range(numCols - 1):
            for k in range(j + 1, numCols):
                # Check if the subarray [1 1] is present
                if matrix[i, j] == 1 and matrix[i, k] == 1:
                    result = 1
                    return result  # Exit the function as we have found a match
    
    return result
#==============================================================================

#=====================================================================================================
def correlationFunction(signal, delay, flag):
    """
    The function correlationFunction(signal, delay, flag) is part of the System
    Identification Package for polynomial models. Its purpose is to calculate
    the correlation function of a signal, as follows:
    
    Inputs:
        signal ==> vector for which the correlation function will be calculated
        
        delay  ==> maximum signal shift for calculating the correlation function
        
        flag   ==> if flag = 1, the correlation function is plotted
    
    Outputs:
        H      ==> vector of lags used for calculating the correlation function
        Y      ==> correlation vector for the lags in H
    
    """
    
    # Verify the inputs and outputs
    # --------------------------------------------------------------------------
    if signal is None or delay is None or flag is None:
        raise ValueError('The function requires 3 inputs')
    
    # --------------------------------------------------------------------------
    # Verify the dimension of the signal and adjust if necessary
    # --------------------------------------------------------------------------
    if signal.ndim > 1 and signal.shape[1] > signal.shape[0]:
        signal = signal.T
    
    # --------------------------------------------------------------------------
    # Calculate the correlation and store in vectors, for each of the delays
    # --------------------------------------------------------------------------
    H = zeros(delay - 1)
    Y = zeros(delay - 1)
    
    for n in range(1, delay):
        H[n - 1] = n - 1
        #r = dot(signal.T, roll(signal, n - 1, axis=0))
        r = correla(signal,roll(signal, n - 1))
        Y[n - 1] = r
    
    # --------------------------------------------------------------------------
    # Normalize the data between -1 and 1
    # --------------------------------------------------------------------------
    if max(Y) > 1:
        Y = Y / max(Y)
    
    # --------------------------------------------------------------------------
    # Plot the data, if flag is equal to 1
    # --------------------------------------------------------------------------
    if flag == 1:
        figure()
        plot(H, Y)
        axhline(y=0.08, color='red', linestyle='--', label='+0.08 Threshold')
        axhline(y=-0.08, color='red', linestyle='--', label='-0.08 Threshold')
        title('Correlation Function')
        xlabel('Delay')
        ylabel('Correlation')
        legend(['Correlation Function', '+0.08 Threshold', '-0.08 Threshold'])
        grid(True)
        box(True)
        show()
    
    return H, Y
#==============================================================================

#=====================================================================================================
def buildStaticResponse(staticModel, u, y):
    """
    The function buildStaticResponse(staticModel, u, y)
    is part of the Bi-Objective System Identification Package for polynomial models. Its purpose
    is to simulate the static model and construct the static regressors' matrix, as follows:
    
    Inputs:
             staticModel ==> matrix containing the grouping of terms and their coefficients,
                            generated by the groupcoef.m function
    
                       u ==> static input
                       y ==> output data
    
    Outputs:
                    yest ==> simulated output for the static model for models where yi has
                            a degree of nonlinearity equal to or greater than 2, with or
                            without cross terms.
    --------------------------------------------------------------------------
    Note: When the degree of nonlinearity of yi is less than or equal to 1,
    including cross terms, use the function
    
    [yest, eqest] = displayStaticModel(staticModel, u, p);
    --------------------------------------------------------------------------
                    Pest ==> static data matrix
    EstimatedParameters ==> vector of static model parameters
    
    """
    
    # Verify the dimension of the input and output of the function
    #--------------------------------------------------------------------------
    if staticModel is None or u is None or y is None:
        raise ValueError('The function requires 3 inputs')
    
    # Verify the compatibility of the dimensions of the input and output vectors
    #--------------------------------------------------------------------------
    ui = array(u)
    yi = array(y)
    if ui.ndim == 1:
        ui = ui[:, newaxis]
    if yi.ndim == 1:
        yi = yi[:, newaxis]
    
    if ui.shape[0] != yi.shape[0]:
        raise ValueError('The vectors must have the same dimension')
    
    # Initialize the variables for building the static matrix
    #--------------------------------------------------------------------------
    rows, cols = staticModel.shape
    value = zeros((ui.shape[0], cols - 1))
    Pest = zeros((ui.shape[0], rows))
    
    # Build the static matrix
    #--------------------------------------------------------------------------
    if cols - 1 == 1:
        linear1 = staticModel[:, :-1] == 0
        # Verify if it is linear or not
        #----------------------------------------------------------------------
        if linear1[0] == 0:
            yest = staticModel[0, -1] * ui / (1 - staticModel[1, -1])
            EstimatedParameters = staticModel[:, -1]
            Pest = hstack((ones(ui.shape), ui))
        else:
            for i in range(rows):
                for j in range(cols - 1):
                    if staticModel[i, j] == 0:
                        value[:, j] = ones(ui.shape[0])
                    elif staticModel[i, j] == 1:
                        value[:, j] = yi[:, 0]
                    elif staticModel[i, j] == 2:
                        value[:, j] = ui[:, 0]
                Pest[:, i] = prod(value, axis=1) * staticModel[i, -1]
            EstimatedParameters = staticModel[:, -1]
            yest = sum(Pest, axis=1)
    else:
        for i in range(rows):
            for j in range(cols - 1):
                if staticModel[i, j] == 0:
                    value[:, j] = ones(ui.shape[0])
                elif staticModel[i, j] == 1:
                    value[:, j] = yi[:, 0]
                elif staticModel[i, j] == 2:
                    value[:, j] = ui[:, 0]
            Pest[:, i] = prod(value, axis=1) * staticModel[i, -1]
        EstimatedParameters = staticModel[:, -1]
        yest = sum(Pest, axis=1)
    
    return yest.reshape(-1,1), Pest, EstimatedParameters.reshape(-1,1)
#==============================================================================

#=====================================================================================================
def buildStaticModelAgroup(staticModel):
    """
    The function buildStaticModelAgroup(staticModel) is an auxiliary function
    part of the Bi-Objective System Identification Package for polynomial models.
    Its purpose is to display the static model in string format, allowing the user
    to visualize the encoded model in terms of input and output
    data when the nonlinearity degree is equal to or more than 2, as follows:
    
    Inputs:
    staticModel ==> matrix model containing the grouping of terms and their
                    respective grouping coefficients
    
    Outputs:
        eqest ==> string containing the equation in string format
    
    """

    # Initialize the string for the final equation
    finalEquation = 'y = '

    # Loop through each row of staticModel
    for i in range(len(staticModel)):
        termStr = ''  # Initialize the term for the current row as empty
        for j in range(len(staticModel[i]) - 1):
            if staticModel[i][j] == 0:
                continue  # Skip zero values
            elif staticModel[i][j] == 1:
                termStr += 'y'  # Replace 1 with 'y'
            elif staticModel[i][j] == 2:
                termStr += 'u'  # Replace 2 with 'u'

        # Add the coefficient (staticModel[i][-1]) to the concatenated term
        if termStr:
            finalEquation += f"{staticModel[i][-1]}*{termStr} + "
        else:
            # If all elements up to end-1 are zero, add only the coefficient
            finalEquation += f"{staticModel[i][-1]} + "

    # Check and manually remove the extra '+ ' at the end
    if len(finalEquation) > 3 and finalEquation[-3:] == ' + ':
        finalEquation = finalEquation[:-3]  # Remove the last 3 characters
    eqest = finalEquation

    return eqest
#=====================================================================================================