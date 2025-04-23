__all__ = ["SFXInference"]

from sfx.core.sfx_object import SFXObject

# from sfx.basis immport SFXProjectors


class SFXInference(SFXObject):

    __slots__ = ["data"]

    def __init__(self, data):
        super().__init__()
        self.data = data


#    def compute_drift(self, basis, mode='Stratonovich', diffusion_mode='Vestergaard'):
#
#         # Select a projection basis - either by specifying it
#        # explicitly with the 'functions' keyword of the 'basis'
#        # argument, or by parsing it among the pre-defined bases
#        # defined in SFI_bases.
#        self.drift_basis = basis
#        self.drift_mode = mode
#
#        # Prepare the functions:
#        self.drift_projectors = TrajectoryProjectors(
#            self.data.inner_product_empirical,
#            funcs,
#            is_interacting
#        )
#
#        # Compute the projection coefficients. Indices m,n... denote
#        # spatial indices; indices i,j.. denote particle indices;
#        # indices a,b,... are used for the tensorial structure of the
#        # projections.
#
#        # The velocity projection coefficients (onto the projectors,
#        # ie the self.drift_projectors.c functions) are given by
#        # Stratonovich integration of x_dot(t) c(x(t)).
#        self.v_projections = jnp.einsum('ma,ab->mb',
#            self.data.inner_product_empirical(
#                self.data.Xdot,
#                self.drift_projectors.b,
#                integration_style = 'Stratonovich'
#            ), self.drift_projectors.H )
#
#        self.v_coefficients = self.drift_projectors.projector_combination(self.v_projections)
#
#
#        if self.drift_mode == 'Stratonovich':
#            # Compute w_alpha = - < D grad c_alpha >
#            if diffusion_mode == 'constant':
#                if self.drift_projectors.is_interacting:
#                    int_D_grad_b = jnp.einsum(
#                    'mn,na->ma',
#                    self.D_average,
#                    self.data.trajectory_integral(
#                        lambda t : jnp.einsum(
#                                'inia->na',
#                                self.drift_projectors.grad_b(self.data.X_ito[t])
#                            )
#                        )
#                    )
#                else:
#                    int_D_grad_b = jnp.einsum('mn,na->ma',self.D_average, self.data.trajectory_integral(lambda t : jnp.einsum('nia->na',self.drift_projectors.grad_b_noninteracting(self.data.X_ito[t]))))
#
#            else:
#                if diffusion_mode == 'MSD':
#                    D_local = self.__D_MSD__
#                    X = self.data.X_strat
#                elif diffusion_mode == 'Vestergaard':
#                    D_local = self.__D_Vestergaard__
#                    X = self.data.X_ito
#                elif diffusion_mode == 'ansatz':
#                    D_local = lambda t : self.D_ansatz(self.data.X_ito[t])
#                    X = self.data.X_ito
#                elif diffusion_mode == 'WeakNoise':
#                    D_local = self.__D_WeakNoise__
#                    X = self.data.X_strat
#                else:
#                    raise KeyError("Invalid diffusion_mode parameter: ",diffusion_mode)
#
#                if self.drift_projectors.is_interacting:
#                    int_D_grad_b = self.data.trajectory_integral(lambda t : jnp.einsum('imn,inia->ma',D_local(t),self.drift_projectors.grad_b(X[t])))
#                else:
#                    int_D_grad_b = self.data.trajectory_integral(lambda t : jnp.einsum('imn,nia->ma',D_local(t),self.drift_projectors.grad_b_noninteracting(X[t])))
#
#            self.w_projections = - jnp.einsum('ma,ab->mb', int_D_grad_b,self.drift_projectors.H)
#            self.w_ansatz,self.w_coefficients = self.drift_projectors.projector_combination(self.w_projections)
#
#            # Reconstruct the drift phi_mu = v_mu + w_mu
#            self.phi_projections = self.w_projections + self.v_projections
#            self.phi_ansatz,self.phi_coefficients = self.drift_projectors.projector_combination(self.phi_projections)
#
#        elif self.drift_mode == 'Ito':
#            self.phi_projections = jnp.einsum('ma,ab->mb',self.data.inner_product_empirical( self.data.Xdot, self.drift_projectors.b, integration_style = 'Ito' ), self.drift_projectors.H )
#            self.phi_ansatz,self.phi_coefficients = self.drift_projectors.projector_combination(self.phi_projections)
#
#            self.w_projections = self.phi_projections - self.v_projections
#            self.w_ansatz,self.w_coefficients = self.drift_projectors.projector_combination(self.w_projections)
#
#    def compute_diffusion(self,basis=None,method='Vestergaard',space_dependent_error=False,regularize=None):
#        self.diffusion_method = method
#        # Select the (noisy) local diffusion matrix estimator:
#        if self.diffusion_method == 'MSD':
#            D_local = self.__D_MSD__
#            integration_style = 'Stratonovich'
#            self.diffusion_error_factor = 1
#        elif self.diffusion_method == 'Vestergaard':
#            D_local = self.__D_Vestergaard__
#            integration_style = 'smooth'
#            self.diffusion_error_factor = 4
#        elif self.diffusion_method == 'WeakNoise':
#            D_local = self.__D_WeakNoise__
#            integration_style = 'Stratonovich'
#            self.diffusion_error_factor = 2
#        else:
#            raise KeyError("Wrong diffusion_method argument:",diffusion_method)
#
#        self.D_average = jnp.einsum('t,tmn->mn',self.data.dt,jnp.array([ jnp.einsum('imn->mn', D_local(t) ) for t in range(len(self.data.t)) ]))/self.data.tauN
#        self.D_average_inv = jnp.linalg.inv(self.D_average)
#
#        self.Lambda = jnp.einsum('t,tmn->mn',self.data.dt,jnp.array([ jnp.einsum('imn->mn', self.__Lambda__(t) ) for t in range(len(self.data.t)) ]))/self.data.tauN
#
#        if basis is not None:
#            # Case of a state-dependent diffusion coefficient: fit the
#            # local estimator with the basis functions.
#            self.diffusion_basis = basis
#
#            # Select a projection basis
#            if hasattr(self.diffusion_basis, "functions"):
#                funcs = self.diffusion_basis.functions
#                is_interacting = self.diffusion_basis['interaction']
#            else:
#                import SFI_bases
#                funcs,is_interacting = SFI_bases.basis_selector(self.diffusion_basis,self.data)
#
#            # Prepare the functions:
#            self.diffusion_projectors = TrajectoryProjectors(self.data.inner_product_empirical,funcs,is_interacting)
#            # Reshape into vectors as inner product allows for only one
#            # non-particle index:
#            D_local_reshaped = [ jnp.array([ flatten_symmetric(Di,self.data.d) for Di in D_local(t) ]) for t in range(len(self.data.t))  ]
#            D_projections_reshaped = jnp.einsum('ma,ab->mb',self.data.inner_product_empirical(D_local_reshaped, self.diffusion_projectors.b, integration_style = integration_style), self.diffusion_projectors.H )
#            # Back to matrix form:
#            self.D_projections = jnp.array([ inflate_symmetric(Di,self.data.d) for Di in D_projections_reshaped.T]).T
#            self.D_ansatz_nonreg,self.D_coefficients = self.diffusion_projectors.projector_combination(self.D_projections)
#
#            if regularize is not None:
#                # Regularize the diffusion: anything too close to zero
#                # will be truncated to the typical error.
#                D_average_sqrt = sqrtm(self.D_average)
#                D_average_sqrtinv = sqrtm(jnp.linalg.inv(self.D_average))
#                def D_reg(X):
#                    D_in = self.D_ansatz_nonreg(X)
#                    D_in_norm = jnp.einsum('mn,ino,op->imp',D_average_sqrtinv, D_in ,D_average_sqrtinv)
#                    D_out_norm = []
#                    for Di in D_in_norm:
#                        evals,evecs = jnp.linalg.eigh(Di)
#                        evals_truncated = jnp.array([ max( min( cutoff_high, v ), cutoff_low ) for v in evals ])
#                        D_out_norm.append(jnp.einsum('mn,n,on->mo',evecs,evals_truncated,evecs))
#                    D_out = jnp.einsum('mn,ino,op->imp', D_average_sqrt, jnp.array(D_out_norm), D_average_sqrt )
#                    return D_out
#                self.D_ansatz = D_reg
#            else:
#                self.D_ansatz = self.D_ansatz_nonreg
#
#            self.D_inv_ansatz = lambda X : jnp.linalg.inv(self.D_ansatz(X))
#
#            # Defining a derivative-based ansatz for div D:
#            def divD(x):
#                if self.diffusion_projectors.is_interacting:
#                    return jnp.einsum('mna,jmia->in', self.D_coefficients, self.diffusion_projectors.grad_b(x) )
#                else:
#                    return jnp.einsum('mna,mia->in', self.D_coefficients, self.diffusion_projectors.grad_b_noninteracting(x) )
#            self.divD_ansatz = divD
#
#        if space_dependent_error:
#            Lambda_local_reshaped = [ jnp.array([ flatten_symmetric(Lambda_i,self.data.d) for Lambda_i in Lambda]) for Lambda in Lambda_local ]
#            Lambda_projections_reshaped = jnp.einsum('ma,ab->mb',self.data.inner_product_empirical(Lambda_local_reshaped, self.diffusion_projectors.b, integration_style = 'Ito'), self.diffusion_projectors.H )
#            self.Lambda_projections = jnp.array([ inflate_symmetric(Lambda_i,self.data.d) for Lambda_i in Lambda_projections_reshaped.T]).T
#            self.Lambda_ansatz,self.Lambda_coefficients = self.diffusion_projectors.projector_combination(self.Lambda_projections)
#
#    def compute_force(self):
#        # Assemble the drift and diffusion divergence:
#        if hasattr(self,'divD_ansatz'):
#            self.F_ansatz = lambda X : self.phi_ansatz(X) - self.divD_ansatz(X)
#        else:
#            print("Assuming constant diffusion, setting the force equal to the drift.")
#            self.F_ansatz = self.phi_ansatz
#
#    def compute_entropy(self):
#        if hasattr(self,'D_ansatz'):
#            def dS(t):
#                v = self.v_ansatz(self.data.X_ito[t])
#                return jnp.einsum('imn,im,in->',self.D_inv_ansatz(self.data.X_ito[t]),v,v)
#            self.Sdot =  self.data.trajectory_integral( dS )
#        else:
#            print("Computing entropy production assuming constant diffusion")
#            self.Sdot = jnp.einsum('ma,na,mn->',self.v_projections ,self.v_projections, self.D_average_inv)
#
#        # Per-particle rates:
#        Nb = jnp.prod(self.v_projections.shape)
#        self.Sdot_bias = 2 * Nb /self.data.tauN
#        self.Sdot_error = (2 * self.Sdot/self.data.tauN  + self.Sdot_bias**2 )**0.5
#        self.DeltaS = self.Sdot * self.data.tauN
#        self.error_DeltaS = self.Sdot_error * self.data.tauN
#
#    def compute_drift_error(self,maxpoints=100):
#        indices = jnp.array([ i for i in range(0,len(self.data.X_ito),len(self.data.X_ito)//(1+maxpoints//self.data.jnp.rticles[0]) + 1) ])
#        tauN_sample = sum( self.data.dt[t] * self.data.jnp.rticles[t] for t in indices )
#
#        if hasattr(self,'D_ansatz'):
#            Dinv_Ito   = [ self.D_inv_ansatz(self.data.X_ito[i]) for i in indices ]
#            ansatz_phi_Ito = [ self.phi_ansatz(self.data.X_ito[i]) for i in indices ]
#            self.drift_information = 0.25 * sum([ self.data.dt[t]*jnp.einsum('imn,im,in->',Dinv_Ito[t],ansatz_phi_Ito[t],ansatz_phi_Ito[t]) for t in range(len(indices))]) * ( self.data.tauN / tauN_sample )
#
#        else:
#            print("Computing error assuming constant diffusion.")
#            if not hasattr(self,'D_average'):
#                self.compute_diffusion(basis=None)
#            self.drift_information = 0.25 * jnp.einsum('ma,na,mn->',self.phi_projections ,self.phi_projections, self.D_average_inv) * self.data.tauN
#
#        self.error_drift_information = ( 2 * self.drift_information + jnp.prod(self.phi_projections.shape)**2 / 4 ) ** 0.5
#
#        # Squared typical error due to trajectory length
#        self.drift_trajectory_length_error = 0.5 * jnp.prod(self.phi_projections.shape) / self.drift_information
#
#        # Squared typical error due to time discretization (estimate assuming constant diffusion)
#        def b_grad_b(X):
#            if self.drift_projectors.is_interacting:
#                # b_alpha partial_mu b_beta (X)
#                return jnp.einsum('ia,imib->imab',self.drift_projectors.b(X),self.drift_projectors.grad_b(X))
#            else:
#                return jnp.einsum('ia,mib->imab',self.drift_projectors.b(X),self.drift_projectors.grad_b_noninteracting(X))
#
#        FgradF = [ jnp.einsum('imab,ma,nb->in',b_grad_b(self.data.X_ito[ind]),self.phi_coefficients,self.phi_coefficients) for ind in indices ]
#        av_FgradF_squared = jnp.einsum('tmn->mn',jnp.array([ jnp.einsum('in,im->mn',FgradF[ind],FgradF[ind])*self.data.dt[t]**3 for ind,t in enumerate(indices)])) / tauN_sample
#        self.drift_discretization_error_bias = 0.25 * jnp.einsum('mn,mn->',av_FgradF_squared,self.D_average_inv) / ( 4 * self.drift_information / self.data.tauN )
#
#        self.drift_projections_self_consistent_error = self.drift_trajectory_length_error + self.drift_discretization_error_bias
#
#        # Compute the hierarchical increments of the information when
#        # adding the functions one by one [uses the upper triangular
#        # structure of the projection matrix].
#        self.partial_information = jnp.einsum('ma,na,mn->a',self.phi_projections ,self.phi_projections, self.D_average_inv)*self.data.tauN/4
#        self.cumulative_information = [ self.partial_information[0]]
#        for i in self.partial_information[1:]:
#            self.cumulative_information.append(i+self.cumulative_information[-1])
#        self.cumulative_information = jnp.array(self.cumulative_information)
#        self.cumulative_error = jnp.array([ ( 2*I + (self.data.d*(n+1))**2/4 )**0.5 for n,I in enumerate( self.cumulative_information ) ])
#        self.cumulative_bias = jnp.array([ self.data.d * n/4 for n,I in enumerate(self.cumulative_information)])
#
#    def compute_diffusion_error(self,maxpoints=100):
#        # Estimate the squared error on the inferred D.
#        # 1. due to trajectory length (lack of data):
#        self.diffusion_trajectory_length_error = self.diffusion_error_factor * jnp.prod(self.D_projections.shape) / ( 1.* sum(self.data.jnp.rticles))
#
#        # 2. due to time discretization:
#        indices = jnp.array([ i for i in range(0,len(self.data.X_ito),len(self.data.X_ito)//(1+maxpoints//self.data.jnp.rticles[0]) + 1) ])
#        ansatz_divD = [ self.divD_ansatz(self.data.X_ito[ind]) for ind in indices ]
#        Dinv = jnp.linalg.inv(self.D_average)
#        self.spurious_capacity = 0.25 * jnp.einsum('tmn,nm->',jnp.array([ jnp.einsum('in,im->mn',ansatz_divD[ind],ansatz_divD[ind])*self.data.dt[t] for ind,t in enumerate(indices)]),Dinv) / sum( self.data.dt[t] * self.data.jnp.rticles[t] for t in indices )
#        self.diffusion_discretization_error_bias = (2 * self.spurious_capacity * self.data.dt.mean() )**2
#
#        self.diffusion_projections_self_consistent_error = self.diffusion_trajectory_length_error + \
#                                                           self.diffusion_discretization_error_bias
#        # 3. Contribution coming from the force:
#        #     (4 * Capacity * dt)**2
#        # if the diffusion method is 'MSD' or 'Vestergaard', and of the
#        # form (smaller)
#        #     (Inflow_rate * dt / 2)**2
#        # with the 'WeakNoise' method.
#        if hasattr(self,'w_projections')  and self.diffusion_method == 'WeakNoise':
#            inflow_approx = jnp.einsum('ma,na,mn->',self.w_projections,self.w_projections,self.D_average_inv)
#            self.diffusion_drift_error = (inflow_approx * self.data.dt.mean()/2)**2
#            self.diffusion_projections_self_consistent_error += self.diffusion_drift_error
#        elif hasattr(self,'drift_information') and self.diffusion_method != 'WeakNoise':
#            self.diffusion_drift_error = (4*self.drift_information * self.data.dt.mean() / self.data.tauN)**2
#            self.diffusion_projections_self_consistent_error += self.diffusion_drift_error
#        else:
#            print("No drift information to compute its influence on diffusion error")
#
#    def adaptive_drift_truncation(self,nsigmas=2):
#        """Truncate the basis to minimize overfitting. Uses the criterion of
#        minimizing
#        Ihat - bias - nsigmas * delta Ihat
#        with Ihat the inferred information and delta_Ihat the error on
#        it. Note that this procedure depends on the order in which the
#        functions are provided.
#        """
#        if not hasattr(self,'partial_information'):
#            self.compute_drift_error()
#        (self.I_opt,self.n_opt) = max( (i,n+1) for n,i in enumerate(self.cumulative_information-self.cumulative_bias-nsigmas*self.cumulative_error))
#        self.phi_projections = self.phi_projections[:,:self.n_opt]
#        self.phi_ansatz,self.phi_coefficients = self.drift_projectors.truncated_projector_combination(self.phi_projections)
#
#    def print_report(self):
#        """ Tell us a bit about yourself.
#        """
#        print("             ")
#        print("  --- StochasticForceInference report --- ")
#        print("Average diffusion tensor:\n",self.D_average)
#        if hasattr(self,'DeltaS'):
#            print("Entropy production: inferred/bootstrapped error",self.DeltaS,self.error_DeltaS)
#        if hasattr(self,'drift_projections_self_consistent_error'):
#            print("Drift information: inferred/bootstrapped error",self.drift_information,self.error_drift_information)
#            print("Drift: squared typical error on projections:",self.drift_projections_self_consistent_error)
#            print("  - due to trajectory length:",self.drift_trajectory_length_error)
#            print("  - due to discretization:",self.drift_discretization_error_bias)
#        if hasattr(self,'diffusion_projections_self_consistent_error'):
#            print("Diffusion: squared typical error on projections:",self.diffusion_projections_self_consistent_error)
#            print("  - due to trajectory length:",self.diffusion_trajectory_length_error)
#            print("  - due to discretization:",self.diffusion_discretization_error_bias)
#            if hasattr(self,'diffusion_drift_error'):
#                print("  - due to drift:",self.diffusion_drift_error)
#
#
#    def provide_diffusion(self,D,divD=None):
#        """Provide external values for the diffusion parameters to bypass
#        their inference - either as a function or as constant.
#        """
#        self.diffusion_error_factor = 0
#
#        if hasattr(D,'shape'):
#            self.D_average = D
#            self.D_average_inv = jnp.linalg.inv(D)
#        else:
#            self.D_ansatz = D
#            self.divD_ansatz = divD
#            self.D_inv_ansatz = lambda X : jnp.linalg.inv(self.D_ansatz(X))
#            self.D_average = jnp.einsum('t,tmn->mn',self.data.dt,jnp.array([ jnp.einsum('imn->mn', D(self.data.X_ito[t]) ) for t in range(len(self.data.t)) ]))/self.data.tauN
#            self.D_average_inv = jnp.linalg.inv(self.D_average)
#
#    def compare_to_exact(self,data_exact=None,drift_exact=None,force_exact=None,D_exact=None,divD_exact=None,verbose=True,maxpoints = 1000):
#        """This routine is designed for tests with artificial data where the
#        exact model is known. It will compute the mean squared error
#        between inferred and exact drift/force/diffusion.
#        """
#
#        if data_exact is None:
#            # In the case of noisy ijnp.t data, we want to compare to
#            # the force inferred on the real trajectory, not the noisy
#            # one (which would use values of the force field that
#            # weren't explored by the trajectory, and thus cannot be
#            # predicted).
#            self.data_exact = self.data
#        else:
#            self.data_exact = data_exact
#
#        indices = jnp.array([ i for i in range(0,min(len(self.data_exact.t),len(self.data.t)),len(self.data.X_ito)//(1+maxpoints//self.data.jnp.rticles[0]) + 1) ])
#        if verbose:
#            print("Comparing to exact data...")
#
#        if hasattr(self,'F_ansatz') and force_exact is not None:
#            self.exact_F_Strat = [ force_exact(self.data_exact.X_strat[i]) for i in indices ]
#            self.exact_F_Ito = [ force_exact(self.data_exact.X_ito[i]) for i in indices ]
#            self.ansatz_F_Ito   = [ self.F_ansatz(self.data_exact.X_ito[i]) for i in indices ]
#
#            # Compute the MSE along the trajectory. Data is scaled by
#            # the average diffusion for dimensional correctness.
#            self.MSE_F = sum([jnp.einsum('im,in,mn->',self.exact_F_Ito[i]-self.ansatz_F_Ito[i],self.exact_F_Ito[i]-self.ansatz_F_Ito[i],self.D_average_inv) for i,t in enumerate(indices) ]) / sum([jnp.einsum('im,in,mn->',self.ansatz_F_Ito[i],self.ansatz_F_Ito[i],self.D_average_inv) for i,t in enumerate(indices)])
#            if verbose:
#                print("Mean squared error on force:",self.MSE_F)
#
#        if hasattr(self,'phi_ansatz') and drift_exact is not None:
#            self.ansatz_phi_Ito = [ self.phi_ansatz(self.data_exact.X_ito[i]) for i in indices ]
#            self.exact_phi_Ito = [ drift_exact(self.data_exact.X_ito[i]) for i in indices ]
#            self.MSE_drift = sum([jnp.einsum('im,in,mn->',self.exact_phi_Ito[i]-self.ansatz_phi_Ito[i],self.exact_phi_Ito[i]-self.ansatz_phi_Ito[i],self.D_average_inv) for i,t in enumerate(indices)]) / sum([jnp.einsum('im,in,mn->',self.ansatz_phi_Ito[i],self.ansatz_phi_Ito[i],self.D_average_inv) for i,t in enumerate(indices)])
#            if verbose:
#                print("Mean squared error on drift:",self.MSE_drift)
#
#        if D_exact is not None:
#            if hasattr(D_exact,'shape'):
#                self.exact_D =    [ jnp.array([ D_exact for j in range(self.data_exact.X_ito[i].shape[0])]) for i in indices ]
#            else:
#                self.exact_D =    [ D_exact(self.data_exact.X_ito[i]) for i in indices ]
#            if hasattr(self,'D_ansatz'):
#                self.ansatz_D   = [ self.D_ansatz(self.data_exact.X_ito[i]) for i in indices ]
#            else:
#                self.ansatz_D   = [ jnp.array([ self.D_average for j in range(self.data_exact.X_ito[i].shape[0])]) for i in indices ]
#            self.MSE_D = sum([jnp.einsum('imn,iop,no,pm->',self.exact_D[i]-self.ansatz_D[i],self.exact_D[i]-self.ansatz_D[i],self.D_average_inv,self.D_average_inv) for i,t in enumerate(indices)]) / sum([jnp.einsum('imn,iop,no,pm->',self.ansatz_D[i],self.ansatz_D[i],self.D_average_inv,self.D_average_inv) for i,t in enumerate(indices)])
#            if verbose:
#                print("Mean squared error on diffusion:",self.MSE_D)
#
#        if hasattr(self,'DeltaS') and D_exact is not None  and force_exact is not None:
#            # Compute the heat and information:
#            if hasattr(D_exact,'shape'):
#                self.exact_Heat = jnp.einsum('t,nm,tmn->', data_exact.dt,jnp.linalg.inv(D_exact),
#                    jnp.array([ jnp.einsum('im,in->mn',force_exact(self.data_exact.X_strat[t]),
#                                         data_exact.dX_plus[t]/data_exact.dt[t]) for t in range(len(data_exact.dt))]))
#            else:
#                self.exact_Heat = jnp.einsum('t,t->', data_exact.dt,
#                    jnp.array([ jnp.einsum('imn,im,in->',jnp.linalg.inv(D_exact(data_exact.X_strat[t])),
#                    force_exact(self.data_exact.X_strat[t]),data_exact.dX_plus[t]/data_exact.dt[t]) for t in range(len(data_exact.dt))]))
#            print("Exact heat / inferred entropy production:",self.exact_Heat,self.DeltaS)
#
#
#
#
#    def simulate_bootstrapped_trajectory(self,oversampling=1):
#        """Simulate an overdamped Langevin trajectory with the inferred
#        ansatz force field and similar time series and initial
#        conditions as the ijnp.t data.
#        """
#        from SFI_langevin import OverdampedLangevijnp.ocess
#        if hasattr(self,'D_ansatz'):
#            return OverdampedLangevijnp.ocess(self.phi_ansatz, self.D_ansatz, self.data.t, initial_position = 1. * self.data.X_ito[0],oversampling=oversampling, mode = 'drift')
#        else:
#            print("Simulating bootstrapped trajectory assuming constant diffusion.")
#            return OverdampedLangevijnp.ocess(self.phi_ansatz, self.D_average, self.data.t, initial_position = 1. * self.data.X_ito[0],oversampling=oversampling, mode = 'drift')
#
#
#    # Local diffusion estimators. All these are local-in-time noisy
#    # estimates of the diffusion tensor (noise is O(1)). Choose it
#    # adapted to the problem at hand.
#    def __D_MSD__(self,t):
#        return jnp.einsum('im,in->imn',self.data.dX_plus[t],self.data.dX_plus[t])/(2*self.data.dt[t])
#
#    def __D_Vestergaard__(self,t):
#        # Local estimator inspired by "Vestergaard CL, Blainey PC,
#        # Flyvbjerg H (2014). Optimal estimation of diffusion
#        # coefficients from single-particle trajectories. Physical
#        # Review E 89(2):022726.".
#        #
#        # It is unbiased with respect to measurement noise, at the
#        # cost of a 4x slower convergence. Use this estimator if
#        # measurement noise is the limiting factor on inferring
#        # D. Note that the error is minimized when symmetrizing the
#        # correction term and integrating in Ito, i.e. evaluating the
#        # projector at the initial point of the interval.
#        return (jnp.einsum('im,in->imn',self.data.dX_plus[t]+self.data.dX_minus[t],self.data.dX_plus[t]+self.data.dX_minus[t])
#            +   jnp.einsum('im,in->imn',self.data.dX_plus[t],self.data.dX_minus[t])
#            +   jnp.einsum('im,in->imn',self.data.dX_minus[t],self.data.dX_plus[t]))  /(4*self.data.dt[t])
#
#
#    def __D_WeakNoise__(self,t):
#        """The "WeakNoise" estimator is an experimental feature. It subtracts
#        the persistent velocity v, computed in the drift inference
#        routine, from the displacement, thus increasing significantly
#        the precision in the case of large dt, strongly
#        out-of-equilibrium systems.
#        """
#        vdt = self.v_ansatz(self.data.X_strat[t])*self.data.dt[t]
#        return jnp.einsum('im,in->imn',self.data.dX_plus[t]- vdt,
#                                      self.data.dX_plus[t]- vdt )/(2*self.data.dt[t])
#
#
#    def _estimate_measurement_error_(self, t, use_v=False):
#        # Lambda term is a local estimator for the measurement
#        # error. It is valid only in the weak drift limit;
#        # specifically, if eta is the random localization error, then
#        #
#        # <Lambda_munu> = <eta_mu eta_nu> - dt^2 <F_mu F_nu>
#        #
#        # i.e. it results in an underestimate (and can even be
#        # negative) if dt is large.
#        L = - (
#        jnp.einsum('im,in->imn',
#                   self.data.dX_plus[t],
#                   self.data.dX_minus[t]
#                   ) + jnp.einsum('im,in->imn',self.data.dX_minus[t],self.data.dX_plus[t]))/2
#        if use_v:
#            v = self.v_ansatz(self.data.X_ito[t])
#            L += self.data.dt[t]**2 * jnp.einsum('im,in->imn',v,v)
#        return  L
