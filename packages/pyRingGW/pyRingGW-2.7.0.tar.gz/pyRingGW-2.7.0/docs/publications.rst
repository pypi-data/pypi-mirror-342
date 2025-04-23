References
-------------

- Methods:

   The code is mainly based on the formalism described in `Carullo et al., arXiv:1902.07527 <https://arxiv.org/abs/1902.07527>`_.
   For signals extending below a pure ringdown emission, it uses the truncated formulation of `Isi et al., arXiv:1905.00869 <https://arxiv.org/abs/1905.00869>`_ (see also `their longer follow-up, arXiv:2107.05609 <https://arxiv.org/abs/2107.05609>`_).   
   Additional details on the methodology can be found in the `GWTC-2 Testing GR LVK catalog, arXiv:2010.14529 <https://arxiv.org/abs/2010.14529>`_ and `GWTC-3 Testing GR LVK catalog, arXiv:2112.06861 <https://arxiv.org/abs/2112.06861>`_.

   A pedagogical discussion of models usage and systematic uncertainties can be found in `Gennari et al., arXiv:2312.12515 <https://arxiv.org/abs/2312.12515>`_.

- Additional studies using pyRing:
   * Ringdown signatures of Kerr black holes immersed in a magnetic field: `arXiv:2406.09314 <https://arxiv.org/abs/2406.09314>`_;
   * Simulation based inference in the time domain: `arXiv:2404.11373 <https://arxiv.org/abs/2404.11373>`_;
   * Higher modes GWTC-3 search using a numerical relativity calibrated-model: `arXiv:2312.12515 <https://arxiv.org/abs/2312.12515>`_;
   * Bounds on tidal charges in braneworld gravity: `arXiv:2311.03556 https://arxiv.org/abs/2311.03556`_;
   * Measuring scalar polarization in Einstein scalar Gauss-Bonnet: `arXiv:2212.11359 <https://arxiv.org/abs/2212.11359>`_; 
   * Impact of start time uncertainty on overtone detection in GW150914: `arXiv:2201.00822 <https://arxiv.org/abs/2201.00822>`_, `arXiv:2310.20625 <https://arxiv.org/abs/2310.20625>`_, `arXiv:2305.18528 <https://arxiv.org/abs/2305.18528>`_;
   * GWTC-3 Testing GR LVK catalog: `arXiv:2112.06861 <https://arxiv.org/abs/2112.06861>`_;
   * GW190521 waveforms consistency and astrophysical implications: `arXiv:2112.06856 <https://arxiv.org/abs/2112.06856>`_; 
   * Models and constraints of ringdown in the presence of U(1) black hole charges: `arXiv:2109.13961 <https://arxiv.org/abs/2109.13961>`_;
   * Constraints on braneworld gravity: `arXiv:2106.05558 <https://arxiv.org/abs/2106.05558>`_;
   * Verification of the Bekenstein-Hod bound: `arXiv:2103.06167 <https://arxiv.org/abs/2103.06167>`_;
   * Constraints on alternative theories of gravity using the ParSpec formalism: `arXiv:2102.05939 <https://arxiv.org/abs/2102.05939>`_;  
   * Investigations and observational constraints on the area quantisation hypothesis: `arXiv:2011.03816 <https://arxiv.org/abs/2011.03816>`_; 
   * GW190521 discovery: `arXiv:2009.01075 <https://arxiv.org/abs/2009.01075>`_ and physics implications: `arXiv:2009.01190 <https://arxiv.org/abs/2009.01190>`_;
   * Spectroscopy of Rotating Black Holes Pierced by Cosmic Strings: `arXiv:2002.01695 <https://arxiv.org/abs/2002.01695>`_.
   * Probing the Purely Ingoing Nature of the Black-hole Event Horizon `arXiv:1912.07058 <https://arxiv.org/abs/1912.07058>`_;


- Citing ``pyRing``:

   When referencing ``pyRing`` in your publications, please cite the following papers: `arXiv:1902.07527 <https://arxiv.org/abs/1902.07527>`_, `arXiv:1905.00869 <https://arxiv.org/abs/1905.00869>`_, `arXiv:2010.14529 <https://arxiv.org/abs/2010.14529>`_ and the software Zenodo release:
   
   .. code-block:: bibtex

      @software{pyRing,
      author       = {Carullo, Gregorio and
                     Del Pozzo, Walter and
                     Veitch, John},
      title        = "\texttt{pyRing}: a time-domain ringdown analysis python package",
      month        = jul,
      year         = 2023,
      publisher    = {Zenodo},
      version      = {2.3.0},
      doi          = {10.5281/zenodo.8165508},
      url          = {https://doi.org/10.5281/zenodo.8165508},
      howpublished = "\href{https://git.ligo.org/lscsoft/pyring}{git.ligo.org/lscsoft/pyring}",
      }
   
- External libraries:

   ``pyRing`` relies on a number of open-source packages. 
   If you use the software in your publications, please cite the references found at these links:

   * `corner <https://github.com/dfm/corner.py>`__
   * `cpnest <https://github.com/johnveitch/cpnest>`__
   * `gwpy <https://github.com/gwpy/gwpy>`__
   * `lalsuite <https://git.ligo.org/lscsoft/lalsuite>`__
   * `matplotlib <https://github.com/matplotlib/matplotlib>`__
   * `numpy <https://numpy.org/citing-numpy/>`__
   * `scipy <https://scipy.org/citing-scipy/>`__
   * `pesummary <https://lscsoft.docs.ligo.org/pesummary/stable_docs/citing_pesummary.html>`__
