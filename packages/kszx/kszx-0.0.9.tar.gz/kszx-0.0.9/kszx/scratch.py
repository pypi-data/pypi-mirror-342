    
    def analyze_pgv_chi2(self, field, fnl, bv, nkbins, ddof):
        """Do model parameters (fnl,bv) fit the data? Returns (chi2, ndof, p-value).

        The 'field' argument is a length-2 vector, selecting a linear combination
        of the 90+150 GHz velocity reconstructions. For example:
           - field=[1,0] for 90 GHz
           - field=[0,1] for 150 GHz
           - field=[1,-1] for null (90-150) GHz.

        The 'nkbins' argument is the number of k-bins used to compute the chi^2.

        The 'ddof' argument is used to compute the number of degrees of freedom:
            ndof = nkbins - ddof
        """

        d = self.pgv_data(field)[:nkbins]              # shape (nkbins,)
        s = self._pgv_surr(field, bv, fnl)[:,:nkbins]  # shape (nsurr,nkbins)
        x = d - np.mean(s, axis=0)                     # shape (nkbins,)
        cov = np.cov(s, rowvar=False)                  # shape (nkbins,nkbins)
        
        chi2 = np.dot(x, np.linalg.solve(cov,x))
        ndof = nkbins - ddof
        pte = scipy.stats.chi2.sf(chi2, ndof)
        
        return chi2, ndof, pte

