pymodaq_plugins_template
########################

.. the following must be adapted to your developed package, links to pypi, github  description...

.. image:: https://img.shields.io/pypi/v/pymodaq_plugins_thorlabs.svg
   :target: https://pypi.org/project/pymodaq_plugins_thorlabs/
   :alt: Latest Version

.. image:: https://readthedocs.org/projects/pymodaq/badge/?version=latest
   :target: https://pymodaq.readthedocs.io/en/stable/?badge=latest
   :alt: Documentation Status

.. image:: https://github.com/PyMoDAQ/pymodaq_plugins_thorlabs/workflows/Upload%20Python%20Package/badge.svg
   :target: https://github.com/PyMoDAQ/pymodaq_plugins_thorlabs
   :alt: Publication Status

PyMoDAQ plugins for the ACS motion control unit.

Authors
=======

* Jérémie Margueritat  (jeremie.margueritat@univ-lyon1.fr)

Instruments
===========

Below is the list of instruments included in this plugin

Actuators
+++++++++

* **ACS motion control**: control up to 8 stages.

It has been developped with ACS motion control unit: SPiiPlusEC, linked with a two axis driver (amplifier) UDMnt. 
The stages were alio's translation stages  AI-CM-6000-XY   

Installation instructions
=========================
The user as to install the drivers from ACS. He may also need to intialise the stage within the software with the buffer file provided by ACS.

* PyMoDAQ’s version: developed with PyMoDAQ 5.0.5
* Operating system’s version: Windows 11 
* The plugin assumes that the acs drivers are installed. 