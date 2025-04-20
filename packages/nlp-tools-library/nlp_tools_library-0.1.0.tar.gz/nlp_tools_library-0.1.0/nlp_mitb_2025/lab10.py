class HMMTextClassifier:
    def __init__(self, n_components=3):
        """Initialize the HMMTextClassifier with the specified number of hidden states."""
        self.n_components = n_components
        
        try:
            from sklearn.datasets import fetch_20newsgroups
            from hmmlearn import hmm
            from sklearn.feature_extraction.text import CountVectorizer
            from sklearn.metrics import accuracy_score
            from sklearn.naive_bayes import GaussianNB
            from sklearn.model_selection import train_test_split
            
            self.fetch_20newsgroups = fetch_20newsgroups
            self.hmm = hmm
            self.CountVectorizer = CountVectorizer
            self.accuracy_score = accuracy_score
            self.GaussianNB = GaussianNB
            self.train_test_split = train_test_split
            
            self.model = None
            self.vectorizer = None
        except ImportError:
            raise ImportError("Required packages not installed. Please install sklearn, hmmlearn.")
    
    def fit(self, texts, categories=None):
        """Fit the HMM model on the provided texts."""
        if categories:
            data = self.fetch_20newsgroups(categories=categories, remove=('headers', 'footers', 'quotes'))
            texts = data.data
        
        self.vectorizer = self.CountVectorizer()
        X = self.vectorizer.fit_transform(texts).toarray()
        
        self.model = self.hmm.GaussianHMM(n_components=self.n_components, covariance_type="diag")
        self.model.fit(X)
        return self
    
    def predict(self, texts):
        """Predict using the fitted HMM model."""
        if not self.model or not self.vectorizer:
            raise ValueError("Model not fitted yet. Call fit() first.")
            
        X = self.vectorizer.transform(texts).toarray()
        return self.model.predict(X)
    
    def create_hybrid_model(self, texts, labels, test_size=0.2, random_state=42):
        """Create a hybrid model combining HMM features with Naive Bayes classification."""
        self.vectorizer = self.CountVectorizer()
        X = self.vectorizer.fit_transform(texts).toarray()
        
        # Train HMM to extract features
        self.model = self.hmm.GaussianHMM(n_components=self.n_components, covariance_type="diag")
        self.model.fit(X)
        features = self.model.predict(X).reshape(-1, 1)
        
        # Train Naive Bayes on HMM features
        X_train, X_test, y_train, y_test = self.train_test_split(
            features, labels, test_size=test_size, random_state=random_state
        )
        
        self.nb_model = self.GaussianNB()
        self.nb_model.fit(X_train, y_train)
        
        preds = self.nb_model.predict(X_test)
        accuracy = self.accuracy_score(y_test, preds)
        
        return accuracy, self.nb_model
