<h1 align="center">GSEWidgets</h1>

GSEWidgets is a package that makes use of Qt6 to create some easy to use and define widgets. This is achieved by 
combining the functionality of PyQt6 and qtpy libraries. Most of the custom widgets are created to be used
with specific applications developed for GSECARS.

## Installation

GSEWidgets requires the use of Python 3.10 or higher. In some cases lower versions are also accepted,
but version 3.10 is recommended for best compatibility. See the full [requirements list](#urequirementsu)
for the GSEWidgets package.

<br />

#### <u>PyPI</u>
To install from PyPI use:
````
pip install gsewidgets
````
<br />

#### <u>Source</u>
To install from source first download the project from the package 
[releases](https://github.com/GSECARS/GSEWidgets/releases) 
or use: 
````
git clone https://github.com/GSECARS/GSEWidgets.git
````
Move into the project directory: 
````
cd GSEWidgets
````
Install using pip: 
````
pip install .
````

<br />

#### <u>Requirements</u>
1. Python >= 3.10
2. PyQt6 >= 6.4.0
3. qtpy >= 2.2.1

<br />

## Available widgets

- ErrorMessageBox
- VerticalLine
- HorizontalLine
- Label
- FlatButton
- FileBrowserButton
- DirectoryBrowserButton
- ColorDialogButton
- NumericSpinBox
- NoWheelNumericSpinBox
- InputBox
- FilePathInputBox
- FileNameInputBox
- URIInputBox
- FullComboBox
- CheckBox
- ToggleCheckBox
- XYZCollectionPointsTable

Here is a screenshot with an example application, one using custom styles in .qss files.

<p><img alt="Example widgets" src="gsewidgets/examples/assets/images/gsewidgets_example.png"></p>

The example application is also packaged and can be used after the installation. See below:
````
from gsewidgets.examples import app
app.run()
````

<br />

## License

GSEWidgets is distributed under the GNU General Public License version 3. You should have 
received a copy of the GNU General Public License along with this program.  If not, see 
<https://www.gnu.org/licenses/>.

<br />

[Christofanis Skordas](mailto:skordasc@uchicago.edu) - Last updated: 31-Mar-2023 