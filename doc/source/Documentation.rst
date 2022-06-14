.. _Documentation:

*******************************
Generating Sphinx Documentation
*******************************

This documentation is generated using ``sphinx``, supported formats are HTML and TeX/LaTeX (in PDF). ``sphinx`` and its dependencies can be installed using ``spack-stack``
and the environment spec ``jedi-tools-env`` (see :numref:`Section %s <Environments>`). Note that in order to generated TeX/LaTeX documentation, a TeX/LaTeX distribution is required as external package (see :numref:`Section %s <Prerequisites_Texlive>`), and the ``jedi-tools-env`` environment spec must be built with the variant ``+latex``.

Steps to generate the documentation locally:

1. If using a ``spack-stack`` environment, load the required modules (e.g. ``module load jedi-tools-env``), otherwise make sure that ``sphinx``is loaded, ``sphinxcontrib-bibtex`` and your TeX/LaTeX distribution of choice are optionally loaded into your environment. The latter two are only required if building the TeX/LaTeX documentation.

2. Execute the following commands (note that the default value for option ``SPHINX_OUTPUT_HTML`` is ``ON``, and for option ``SPHINX_OUTPUT_LATEX`` is ``OFF``):

.. code-block:: console

   cd doc
   mkdir build
   cd build
   cmake [-DSPHINX_OUTPUT_HTML=OFF] [-DSPHINX_OUTPUT_LATEX=ON] ..
   make

3. The output can be found in subdirectories ``html`` (``open html/index.html``) and ``pdf`` (open ``pdf/spack-stack.pdf``).

.. note::
   If updates to the documentation source files in ``doc/source`` are made, rerunning ``make`` updates the HTML documentation, but not the TeX/LaTeX documentation. To update the latter, run ``make clean`` followed by ``make``.
