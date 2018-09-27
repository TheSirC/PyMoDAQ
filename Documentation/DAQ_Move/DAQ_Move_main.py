
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSlot, QThread, pyqtSignal, QLocale
import sys
from PyMoDAQ.DAQ_Move.DAQ_Move_GUI import Ui_Form

import numpy as np
from PyMoDAQ.DAQ_Move import hardware
from PyMoDAQ.DAQ_Move.hardware import DAQ_Move_Stage_type
#check for plugins to be added to the DAQ_Move_Stage_type enum
#must be loeaded to register proper custom parameter types
from pyqtgraph.parametertree import Parameter, ParameterTree
import pyqtgraph.parametertree.parameterTypes as pTypes
import PyMoDAQ.DAQ_Utils.custom_parameter_tree
from PyMoDAQ.DAQ_Utils.DAQ_utils import ThreadCommand
from easydict import EasyDict as edict

class DAQ_Move(Ui_Form,QObject):
    """
        | DAQ_Move object is a module used to control one motor from a specified list.
        |
        | Preset is an optional list of dicts used to preset programatically settings such as the name of the controller from the list of possible controllers, COM address...
        |
        | Init is a boolean to tell the programm to initialize the controller at the start of the programm given the preset options

        ========================= =================================================
        **Attributes**             **Type**
        *command_stage*            instance of pyqtSignal
        *move_done_signal*         instance of pyqtSignal
        *update_settings_signal*   instance of pyqtSignal
        *log_signal*               instance of pyqtSignal
        *bounds_signal*            instance of pyqtSignal
        *params*                   dictionnary list
        *ui*                       instance of UI_Form
        *parent*                   QObject
        *title*                    string
        *wait_time*                int
        *Initialized_state*        boolean
        *Move_done*                boolean
        *controller*               instance of the specific controller object
        *stage*                    instance of the stage (axis or wathever) object
        *current_position*         float
        *target_position*          float
        *wait_position_flag*       boolean
        *stage_types*              string list
        ========================= =================================================

        See Also
        --------
        set_enabled_move_buttons, set_setting_tree, stage_changed, Quit_fun, IniStage_fun, Move_Abs, Move_Rel, Move_Home, Get_position, Stop_Motion, show_settings, show_fine_tuning

        References
        ----------
        QLocale, QObject, pyqtSignal, QStatusBar, ParameterTree
    """
    command_stage=pyqtSignal(ThreadCommand)
    move_done_signal=pyqtSignal(str,float) #to be used in external program to make sure the move has been done, export the current position. str refer to the unique title given to the module
    update_settings_signal=pyqtSignal(edict)
    log_signal=pyqtSignal(str)
    bounds_signal=pyqtSignal(bool)
    params = [
        {'title': 'Main Settings:','name': 'Main_Settings','type': 'group','children':[
            {'title': 'Move type:','name': 'Move_type', 'type': 'str', 'value': '', 'readonly': True},
            {'title': 'Bounds options:','name':'movebounds','type':'group', 'visible': False,'children':[
                    {'title': 'Stop if out of bounds:', 'name': 'stop_bounds', 'type': 'bool', 'value': False},
                    {'title': 'Bound min:', 'name': 'bound_min', 'type': 'float', 'value': 0},
                    {'title': 'Bound max:', 'name': 'bound_max', 'type': 'float', 'value': 10}]},
            ]},
        {'title': 'Move_Settings', 'name': 'Move_Settings', 'type': 'group'}
        ]



    def __init__(self,parent,title="PyMoDAQ Move",preset=None,init=False):

        # DAQ_Move object is a module used to control one motor from a specified list.
        # preset is an optional list of dicts used to preset programatically settings such as the name of the controller from the list of possible controllers, COM address...
        # init is a boolean to tell the programm to initialize the controller at the start of the programm given the preset options

        QLocale.setDefault(QLocale(QLocale.English, QLocale.UnitedStates))
        super(DAQ_Move,self).__init__()

        self.ui=Ui_Form()
        self.ui.setupUi(parent)
        self.ui.Moveto_pb_bis_2.setVisible(False)
        self.parent=parent
        #self.parent.close_signal.connect(self.Quit_fun) #need a drived class to handle this, see form_custom in daq_utils but that was bugging
        self.ui.title_label.setText(title)
        self.title=title
        self.ui.statusbar=QtWidgets.QStatusBar(parent)
        self.ui.StatusBarLayout.addWidget(self.ui.statusbar)
        self.ui.statusbar.setMaximumHeight(20)



        self.wait_time=1000
        self.ui.Ini_state_LED
        self.parent=parent
        self.ui.Ini_state_LED.clickable=False
        self.ui.Ini_state_LED.set_as_false()
        self.ui.Move_Done_LED.clickable=False
        self.ui.Move_Done_LED.set_as_false()
        self.Initialized_state=False
        self.ui.Current_position_sb.setReadOnly(False)
        self.Move_done=False

        self.controller=None #the hardware controller/set after initialization and to be used by other modules
        self.stage=None #the hardware stage/set after initialization and to be used by other modules

        self.current_position=0;
        self.target_position=0;
        self.wait_position_flag=True

        self.ui.Current_position_sb.setValue(self.current_position)
        self.set_enabled_move_buttons(enable=False)
        self.ui.groupBox.hide()
        self.parent.resize(150,200)


        ##Setting stages types
        self.stage_types=DAQ_Move_Stage_type.names()
        self.ui.Stage_type_combo.clear()
        self.ui.Stage_type_combo.addItems(self.stage_types)


        #create main parameter tree
        self.ui.settings_tree = ParameterTree()
        self.ui.verticalLayout_2.addWidget(self.ui.settings_tree)
        self.ui.settings_tree.setMinimumWidth(300)

        self.settings=Parameter.create(name='Settings', type='group', children=self.params)
        self.ui.settings_tree.setParameters(self.settings, showTop=False)

        #connecting from tree
        self.settings.sigTreeStateChanged.connect(self.parameter_tree_changed)#any changes on the settings will update accordingly the detector
        self.ui.settings_tree.setVisible(False)
        self.set_setting_tree()
        QtWidgets.QApplication.processEvents()
        ##Connecting buttons:
        self.ui.Stage_type_combo.currentIndexChanged.connect(self.set_setting_tree)
        self.ui.Stage_type_combo.currentIndexChanged.connect(self.stage_changed)

        self.ui.Quit_pb.clicked.connect(self.Quit_fun)
        self.ui.IniStage_pb.clicked.connect(self.IniStage_fun)

        self.update_status("Ready",wait_time=self.wait_time)
        self.ui.Move_Abs_pb.clicked.connect(lambda: self.Move_Abs(self.ui.Abs_position_sb.value()))
        self.ui.Move_Rel_plus_pb.clicked.connect(lambda: self.Move_Rel(self.ui.Rel_position_sb.value()))
        self.ui.Move_Rel_minus_pb.clicked.connect(lambda: self.Move_Rel(-self.ui.Rel_position_sb.value()))
        self.ui.Find_Home_pb.clicked.connect(self.Move_Home)
        self.ui.Get_position_pb.clicked.connect(self.Get_position)
        self.ui.Stop_pb.clicked.connect(self.Stop_Motion)

        self.ui.parameters_pb.clicked.connect(self.show_settings)
        self.ui.fine_tuning_pb.clicked.connect(self.show_fine_tuning)
        self.ui.Abs_position_sb.valueChanged.connect(self.ui.Abs_position_sb_bis.setValue)
        self.ui.Abs_position_sb_bis.valueChanged.connect(self.ui.Abs_position_sb.setValue)
        self.ui.Moveto_pb_bis.clicked.connect(lambda: self.Move_Abs(self.ui.Abs_position_sb_bis.value()))

        # set preset options
        if preset is not None:
            for preset_dict in preset:
                #fo instance preset_dict=dict(object='Stage_type_combo',method='setCurrentIndex',value=1)
                if hasattr(self.ui,preset_dict['object']):
                    obj=getattr(self.ui,preset_dict['object'])
                    if hasattr(obj,preset_dict['method']):
                        setattr(obj,preset_dict['method'],preset_dict['value'])
            QtWidgets.QApplication.processEvents()
        #initialize the controller if init=True
        if init:
            self.ui.IniStage_pb.click()

    def parameter_tree_changed(self,param,changes):
        """
            | Check eventual changes in the changes list parameter.
            |
            | In case of changed values, emit the signal containing the current path and parameter via update_settings_signal to the connected hardware.

            =============== ====================================    ==================================================
            **Parameters**   **Type**                                **Description**

             *param*         instance of pyqtgraph parameter         The parameter to be checked

             *changes*       (parameter,change,infos) tuple list     The (parameter,change,infos) list to be treated
            =============== ====================================    ==================================================
        """

        for param, change, data in changes:
            path = self.settings.childPath(param)
            if path is not None:
                childName = '.'.join(path)
            else:
                childName = param.name()
            if change == 'childAdded':
                pass

            elif change == 'value':
                self.update_settings_signal.emit(edict(path=path,param=param))

            elif change == 'parent':
                pass

    @pyqtSlot(int)
    def set_setting_tree(self,index=0):
        """
            Set the move settings parameters tree, clearing the current tree and setting the 'Move_Settings' node.

            See Also
            --------
            update_status
        """
        self.stage_name=self.ui.Stage_type_combo.currentText()
        self.settings.child('Main_Settings','Move_type').setValue(self.stage_name)
        try:
            for child in self.settings.child(('Move_Settings')).children():
                child.remove()

            class_=getattr(hardware,'DAQ_Move_'+self.stage_name)
            params=getattr(class_,'params')
            move_params=Parameter.create(name='Move_Settings', type='group', children=params)


            self.settings.child(('Move_Settings')).addChildren(move_params.children())


        except Exception as e:
            self.update_status(str(e), wait_time=self.wait_time,log_type="log")


    @pyqtSlot(int)
    def stage_changed(self,index=0):

        """
            | Update the User Interface from the DAQ_Move_Stage_Type given by the position of index parameter.
            |
            | In case of Kinesis_Flipper hardware, update the Move_abs values to adapt the programm to the hardware, else re-init the Move_abs to default value.

            =============== =========== ====================================================================
            **Parameters**   **Type**    **Description**

             *index*         enum list   DAQ_Move_Stage_Type to be checked (corresponding to hardware type)
            =============== =========== ====================================================================

            See Also
            --------
            Move_Abs
        """
        if index==DAQ_Move_Stage_type['Kinesis_Flipper']: #Kinesis_Flipper
            self.ui.Moveto_pb_bis_2.setVisible(True)
            self.ui.Moveto_pb_bis.clicked.disconnect()
            self.ui.Moveto_pb_bis.clicked.connect(lambda: self.Move_Abs(1))
            self.ui.Moveto_pb_bis_2.clicked.connect(lambda: self.Move_Abs(2))

        else:
            self.ui.Moveto_pb_bis_2.setVisible(False)
            self.ui.Moveto_pb_bis.clicked.disconnect()
            self.ui.Moveto_pb_bis.clicked.connect(lambda: self.Move_Abs(self.ui.Abs_position_sb_bis.value()))

    def show_fine_tuning(self):
        """
          Make GroupBox visible if User Interface corresponding attribute is checked to show fine tuning in.
        """
        if self.ui.fine_tuning_pb.isChecked():
            self.ui.groupBox.show()
        else:
            self.ui.groupBox.hide()

    def show_settings(self):
        """
          Make settings tree visible if User Interface corresponding attribute is checked to show the settings tree in.
        """
        if self.ui.parameters_pb.isChecked():

            self.ui.settings_tree.setVisible(True)
        else:
            self.ui.settings_tree.setVisible(False)

    def Quit_fun(self):
        """
            Leave the current instance of DAQ_Move_Main closing the parent widget.
        """
        # insert anything that needs to be closed before leaving
        try:
            if self.Initialized_state:
                self.ui.IniStage_pb.click()

            self.parent.close() #close the parent widget
            try:
                self.parent.parent().parent().close() #the dock parent (if any)
            except: pass

        except Exception as e:
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(":/Labview_icons/Icon_Library/close2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            msgBox=QtWidgets.QMessageBox(parent=None)
            msgBox.addButton(QtWidgets.QMessageBox.Yes)
            msgBox.addButton(QtWidgets.QMessageBox.No)
            msgBox.setWindowTitle("Error")
            msgBox.setText(str(e)+" error happened when uninitializing the stage.\nDo you still want to quit?")
            msgBox.setDefaultButton(QtWidgets.QMessageBox.Yes)
            ret=msgBox.exec();
            if ret==QtWidgets.QMessageBox.Yes:
                self.parent.close()


    def set_enabled_move_buttons(self,enable=False):
        """
            Set the move buttons enabled (or not) in User Interface from the gridLayout_buttons course.

            =============== ========== ================================================
            **Parameters**   **Type**   **Description**

             *enable*        boolean    The parameter making enable or not the buttons
            =============== ========== ================================================

        """
        Nchildren=self.ui.gridLayout_buttons.count()
        for ind in range(Nchildren):
            widget=self.ui.gridLayout_buttons.itemAt(ind).widget()
            if widget!=None:
                widget.setEnabled(enable)
        self.ui.Moveto_pb_bis.setEnabled(enable)
        self.ui.Abs_position_sb_bis.setEnabled(enable)
        self.ui.Current_position_sb.setEnabled(enable)


    def IniStage_fun(self):
        """
            Init :
                * a DAQ_move_stage instance if not exists
                * a linked thread connected by signal to the DAQ_move_main instance

            See Also
            --------
            set_enabled_move_buttons, DAQ_utils.ThreadCommand, DAQ_Move_stage, DAQ_Move_stage.queue_command, thread_status, DAQ_Move_stage.update_settings, update_status
        """
        try:
            if not self.ui.IniStage_pb.isChecked():
                try:
                    self.set_enabled_move_buttons(enable=False)
                    self.ui.Stage_type_combo.setEnabled(True)
                    self.ui.Ini_state_LED.set_as_false()
                    self.command_stage.emit(ThreadCommand(command="Close"))
                except: pass

            else:
                self.stage_name=self.ui.Stage_type_combo.currentText()
                stage=DAQ_Move_stage(self.stage_name,self.current_position)
                self.stage_thread=QThread()
                stage.moveToThread(self.stage_thread)

                self.command_stage[ThreadCommand].connect(stage.queue_command)
                stage.status_sig[ThreadCommand].connect(self.thread_status)
                self.update_settings_signal[edict].connect(stage.update_settings)

                self.stage_thread.stage=stage
                self.stage_thread.start()


                self.ui.Stage_type_combo.setEnabled(False)
                self.command_stage.emit(ThreadCommand(command="Ini_Stage",attributes=[self.settings.child(('Move_Settings')).saveState(),self.controller,self.stage]))



        except Exception as e:
            self.update_status(str(e),wait_time=self.wait_time,log_type="log")

            self.set_enabled_move_buttons(enable=False)

    @pyqtSlot(ThreadCommand)
    def thread_status(self,status): # general function to get datas/infos from all threads back to the main
        """
            | General function to get datas/infos from all threads back to the main0
            |

            Interpret a command from the command given by the ThreadCommand status :
                * In case of **'Update_status'** command, call the update_status method with status attributes as parameters
                * In case of **'Ini_Stage'** command, initialise a Stage from status attributes
                * In case of **'Close'** command, close the launched stage thread
                * In case of **'Check_position'** command, set the Current_position value from status attributes
                * In case of **'Move_Done'** command, set the Current_position value, make profile of Move_Done and send the move done signal with status attributes
                * In case of **'Move_Not_Done'** command, set the current position value from the status attributes, make profile of Not_Move_Done and send the Thread Command "Move_abs"
                * In case of **'update_settings'** command, create child "Move Settings" from  status attributes (if possible)

            ================ ================= ======================================================
            **Parameters**     **Type**         **Description**

            *status*          ThreadCommand()   instance of ThreadCommand containing two attributes :

                                                 * *command*    str
                                                 * *attributes* list

            ================ ================= ======================================================

            See Also
            --------
            update_status, set_enabled_move_buttons, Get_position, DAQ_utils.ThreadCommand, parameter_tree_changed, raise_timeout
        """
        if status.command=="Update_Status":
            if len(status.attributes)>2:
                self.update_status(status.attributes[0],wait_time=self.wait_time,log_type=status.attributes[1])
            else:
                self.update_status(status.attributes[0],wait_time=self.wait_time)

        elif status.command=="Ini_Stage":
            #status.attributes[0]=edict(initialized=bool,info="", controller=, stage=)
            self.update_status("Stage initialized: {:} info: {:}".format(status.attributes[0]['initialized'],status.attributes[0]['info']),wait_time=self.wait_time,log_type='log')
            if status.attributes[0]['initialized']:
                self.controller=status.attributes[0]['controller']
                self.stage=status.attributes[0]['stage']
                self.set_enabled_move_buttons(enable=True)
                self.ui.Ini_state_LED.set_as_true()
                self.Initialized_state=True
            else:
                self.Initialized_state=False
            if self.Initialized_state:
                self.Get_position()

        elif status.command=="Close":
            try:
                self.update_status(status.attributes[0],wait_time=self.wait_time)
                self.stage_thread.exit()
                self.stage_thread.wait()
                finished=self.stage_thread.isFinished()
                if finished:
                    pass
                    delattr(self,'stage_thread')
                else:
                    self.update_status('thread is locked?!',self.wait_time,'log')
            except Exception as e:
                self.update_status(str(e),log_type="log")
            self.Initialized_state=False

        elif status.command=="Check_position":
            self.ui.Current_position_sb.setValue(status.attributes[0])
            self.current_position=status.attributes[0]

        elif status.command=="Move_Done":
            self.ui.Current_position_sb.setValue(status.attributes[0])
            self.current_position=status.attributes[0]
            self.Move_done=True
            self.ui.Move_Done_LED.set_as_true()
            self.move_done_signal.emit(self.title,status.attributes[0])

        elif status.command=="Move_Not_Done":
            self.ui.Current_position_sb.setValue(status.attributes[0])
            self.current_position=status.attributes[0]
            self.Move_done=False
            self.ui.Move_Done_LED.set_as_false()
            self.command_stage.emit(ThreadCommand(command="Move_Abs",attributes=[self.target_position]))
        elif status.command=='update_settings':
            #ThreadCommand(command='update_settings',attributes=[path,data,change]))
            try:
                self.settings.sigTreeStateChanged.disconnect(self.parameter_tree_changed)#any changes on the settings will update accordingly the detector
            except: pass
            try:
                if status.attributes[2] == 'value':
                    self.settings.child('Move_Settings',*status.attributes[0]).setValue(status.attributes[1])
                elif status.attributes[2] == 'limits':
                    self.settings.child('Move_Settings',*status.attributes[0]).setLimits(status.attributes[1])

            except: pass
            self.settings.sigTreeStateChanged.connect(self.parameter_tree_changed)#any changes on the settings will update accordingly the detector
        elif status.command=='raise_timeout':
            self.raise_timeout()

    def update_status(self,txt,wait_time=0,log_type=None):
        """
            Show the given txt message in the status bar with a delay of wait_time ms if specified (0 by default).

            ================ ========== =================================
            **Parameters**    **Type**   **Description**

             *txt*            string     The message to show

             *wait_time*      int        The delay time of showing

             *log_type*       string     The type of the log
            ================ ========== =================================

        """
        try:
            self.ui.statusbar.showMessage(txt,wait_time)
            if log_type is not None:
                self.log_signal.emit(self.title+': '+txt)
        except Exception as e:
            pass

    def Move_Abs(self,position):
        """
            | Make the move from an absolute position.
            |
            | The move is made if target is in bounds, sending the thread command "Reset_Stop_Motion" and "Move_Abs".

            =============== ========== ===========================================
            **Parameters**   **Type**    **Description**

            *position*        float      The absolute target position of the move
            =============== ========== ===========================================

            See Also
            --------
            update_status, check_out_bounds, DAQ_utils.ThreadCommand
        """
        try:
            if not(position==self.current_position and self.stage_name=="Thorlabs_Flipper"):
                self.ui.Move_Done_LED.set_as_false()
                self.Move_done=False
                self.target_position=position
                self.update_status("Moving",wait_time=self.wait_time)
                self.check_out_bounds(position)
                self.command_stage.emit(ThreadCommand(command="Reset_Stop_Motion"))
                self.command_stage.emit(ThreadCommand(command="Move_Abs",attributes=[position]))


        except Exception as e:
            self.update_status(str(e),log_type="log")

    def check_out_bounds(self,position):
        """
            Emit a bounds signal if the checked position is out of bounds.

            =============== ========== ===========================================
            **Parameters**   **Type**    **Description**

            *position*        float      The position to be checked
            =============== ========== ===========================================
        """
        if self.settings.child('Main_Settings','movebounds','stop_bounds').value():
            if position>self.settings.child('Main_Settings','movebounds','bound_max').value() or position < self.settings.child('Main_Settings','movebounds','bound_min').value():
                self.bounds_signal.emit(True)
                raise Exception("{:s} is out of specified position bounds".format(self.title))


    def Move_Rel(self,rel_position):
        """
            | Make a move from the given relative psition and the current one.
            |
            | The move is done if (current position + relative position) is in bounds sending Threads Commands "Reset_Stop_Motion" and "Move_Done"

            =============== ========== ===================================================
            **Parameters**   **Type**    **Description**

            *position*        float     The relative target position from the current one
            =============== ========== ===================================================

            See Also
            --------
            update_status, check_out_bounds, DAQ_utils.ThreadCommand
        """
        try:
            self.ui.Move_Done_LED.set_as_false()
            self.Move_done=False
            self.target_position=self.current_position+rel_position
            self.update_status("Moving",wait_time=self.wait_time)
            self.check_out_bounds(self.target_position)
            self.command_stage.emit(ThreadCommand(command="Reset_Stop_Motion"))
            self.command_stage.emit(ThreadCommand(command="Move_Rel",attributes=[rel_position]))


        except Exception as e:
            self.update_status(str(e),log_type="log")

    def Move_Home(self):
        """
            Send the thread commands "Reset_Stop_Motion" and "Move_Home" and update the status.

            See Also
            --------
            update_status, DAQ_utils.ThreadCommand
        """
        try:
            self.ui.Move_Done_LED.set_as_false()
            self.Move_done=False
            self.update_status("Moving",wait_time=self.wait_time)
            self.command_stage.emit(ThreadCommand(command="Reset_Stop_Motion"))
            self.command_stage.emit(ThreadCommand(command="Move_Home"))


        except Exception as e:
            self.update_status(str(e),log_type="log")

    def Get_position(self):
        """
            Get the current position from the launched thread via the "Check_position" Thread Command.

            See Also
            --------
            update_status, DAQ_utils.ThreadCommand
        """
        try:
            self.command_stage.emit(ThreadCommand(command="Check_position"))

        except Exception as e:
            self.update_status(str(e),log_type="log")

    def Stop_Motion(self):
        """
            Stop any motion via the launched thread with the "Stop_Motion" Thread Command.

            See Also
            --------
            update_status, DAQ_utils.ThreadCommand
        """
        try:
            self.command_stage.emit(ThreadCommand(command="Stop_Motion"))
        except Exception as e:
            self.update_status(str(e),log_type="log")

    @pyqtSlot()
    def raise_timeout(self):
        """
            Update status with "Timeout occured" statement.

            See Also
            --------
            update_status
        """
        self.update_status("Timeout occured",wait_time=self.wait_time,log_type="log")
        self.wait_position_flag=False


class DAQ_Move_stage(QObject):
    """
        ================== ========================
        **Attributes**      **Type**
        *status_sig*        instance of pyqtSignal
        *hardware*          ???
        *stage_name*        string
        *current_position*  float
        *target_position*   float
        *hardware_adress*   string
        *axis_address*      string
        *motion_stoped*     boolean
        ================== ========================
    """
    status_sig=pyqtSignal(ThreadCommand)

    def __init__(self,stage_name,position):
        super(DAQ_Move_stage,self).__init__()
        self.hardware=None
        self.stage_name=stage_name
        self.current_position=position
        self.target_position=0
        self.hardware_adress=None
        self.axis_address=None
        self.motion_stoped=False

    @pyqtSlot(ThreadCommand)
    def queue_command(self,command=ThreadCommand()):
        """
            Interpret the given Thread Command.
                * In case of **'Ini_Stage'** command, init a stage from command attributes.
                * In case of **'Close'** command, unitinalise the stage closing hardware and emitting the corresponding status signal
                * In case of **'Move_Abs'** command, call the Move_Abs method with position from command attributes
                * In case of **'Move_Rel'** command, call the Move_Rel method with the relative position from the command attributes.
                * In case of **'Move_Home'** command, call the Move_Home method
                * In case of **'Check_position'** command, get the current position from the Check_position method
                * In case of **'Stop_motion'** command, stop any motion via the Stop_Motion method
                * In case of **'Reset_Stop_Motion'** command, set the motion_stopped attribute to false

            =============== =============== ================================
            **Parameters**   **Type**        **Description**

             *command*      ThreadCommand()   The command to be interpreted
            =============== =============== ================================

            See Also
            --------
            DAQ_utils.ThreadCommand, Ini_Stage, Close, Move_Abs, Move_Rel, Move_Home, Check_position, Stop_Motion
        """
        try:
            if command.command=="Ini_Stage":
                status=self.Ini_Stage(*command.attributes)# return edict(initialized=bool,info="", controller=, stage=)
                self.status_sig.emit(ThreadCommand(command=command.command,attributes=[ status,'log']))


            elif command.command=="Close":
                status=self.Close()
                self.status_sig.emit(ThreadCommand(command=command.command,attributes=[status]))

            elif command.command=="Move_Abs":
                self.Move_Abs(*command.attributes)

            elif command.command=="Move_Rel":
                self.Move_Rel(*command.attributes)

            elif command.command=="Move_Home":
                self.Move_Home()

            elif command.command=="Check_position":
                pos=self.Check_position()


            elif command.command=="Stop_Motion":
                self.Stop_Motion()

            elif command.command=="Reset_Stop_Motion":
                self.motion_stoped=False
        except Exception as e:
            self.status_sig.emit(ThreadCommand("Update_Status",[str(e),'log']))


    def Ini_Stage(self,params_state=None,controller=None,stage=None):
        """
            Init a stage updating the hardware and sending an hardware Move_Done signal.

            =============== =================================== ==========================================================================================================================
            **Parameters**   **Type**                             **Description**

             *params_state*  ordered dictionnary list             The parameter state of the hardware class composed by a list representing the tree to keep a temporary save of the tree

             *controller*    one or many instance of DAQ_Move     The controller id of the hardware

             *stage*         instance of DAQ_Move                 Defining axes and motors
            =============== =================================== ==========================================================================================================================

            See Also
            --------
            DAQ_utils.ThreadCommand, DAQ_Move
        """
        status=edict(initialized=False,info="")
        try:
            class_=getattr(hardware,'DAQ_Move_'+self.stage_name)
            self.hardware=class_(self,params_state)


            status.update(self.hardware.Ini_Stage(controller,stage)) #return edict(info="", controller=, stage=)

            self.hardware.Move_Done_signal.connect(self.Move_Done)

            #status.initialized=True
            return status
        except Exception as e:
            self.status_sig.emit(ThreadCommand("Update_Status",[str(e),'log']))
            return status

    @pyqtSlot(edict)
    def update_settings(self,settings_parameter_dict):
        """
            Update settings of hardware with dictionnary parameters in case of "Move_Settings" path, else update attributes with dictionnary parameters.

            =========================  =========== ======================================================
            **Parameters**              **Type**    **Description**

            *settings_parameter_dict*  dictionnary  Dictionnary containing the path and linked parameter
            =========================  =========== ======================================================

            See Also
            --------
            update_settings
        """
        #settings_parameter_dict = edict(path=path,param=param)
        path=settings_parameter_dict['path']
        param=settings_parameter_dict['param']
        if path[0]=='Main_Settings':
            if hasattr(self,path[-1]):
                setattr(self,path[-1],param.value())

        elif path[0]=='Move_Settings':
            self.hardware.update_settings(settings_parameter_dict)

    def Close(self):
        """
            Uninitialize the stage closing the hardware.

        """
        self.hardware.Close()
        return "Stage uninitialized"


    def Move_Abs(self,position):
        """
            Make the hardware absolute move from the given position.

            =============== ========= =======================
            **Parameters**  **Type**   **Description**

            *position*       float     The absolute position
            =============== ========= =======================

            See Also
            --------
            Move_Abs
        """
        self.target_position=position
        pos=self.hardware.Move_Abs(position)


    def Move_Rel(self,rel_position):
        """
            Make the hardware relative move from the given relative position added to the current one.

            ================ ========= ======================
            **Parameters**   **Type**  **Description**

             *position*       float    The relative position
            ================ ========= ======================

            See Also
            --------
            Move_Rel
        """
        self.target_position=self.current_position+rel_position
        pos=self.hardware.Move_Rel(rel_position)


    def Move_Home(self):
        """
            Make the hardware move to the init position.

        """
        self.target_position=0
        self.hardware.Move_Home()


    def Check_position(self):
        """
            Get the current position checking the harware position.

        """
        pos=self.hardware.Check_position()
        return pos


    def Stop_Motion(self):
        """
            Stop hardware motion with motion_stopped attribute updtaed to True and a status signal sended with an "update_status" Thread Command

            See Also
            --------
            DAQ_utils.ThreadCommand, Stop_Motion
        """
        self.status_sig.emit(ThreadCommand(command="Update_Status",attributes=["Motion stoping",'log']))
        self.motion_stoped=True
        self.hardware.Stop_Motion()


    @pyqtSlot(float)
    def Move_Done(self,pos):
        """
            | Send a "Move_Done" Thread Command with the given position as an attribute and update the current position attribute.
            |
            | Check if position reached within epsilon => not necessary this is done within the hardware code see polling for instance

            See Also
            --------
            DAQ_utils.ThreadCommand
        """

        #check if position reached within epsilon=> not necessary this is done within the hardware code see polling for instance
        self.current_position=pos
        self.status_sig.emit(ThreadCommand(command="Move_Done",attributes=[pos]))
        #if self.motion_stoped:
        #    self.status_sig.emit(ThreadCommand(command="Move_Done",attributes=[pos]))
        #else:
        #    if np.abs(self.target_position-pos)>self.hardware.settings.child(('epsilon')).value():
        #        self.status_sig.emit(ThreadCommand("Move_Not_Done",[pos]))
        #    else:
        #        self.status_sig.emit(ThreadCommand("Move_Done",[pos]))

    @pyqtSlot(float)
    def  Move_Stoped(self,pos):
        """
            Send a "Move_Done" Thread Command with the given position as an attribute.

            See Also
            --------
            DAQ_utils.ThreadCommand
        """
        self.status_sig.emit(ThreadCommand("Move_Done",[pos]))





if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget();prog = DAQ_Move(Form,title="test",preset=[dict(object='Stage_type_combo',method='setCurrentText',value='PI')],init=False);Form.show()
    #Form1 = QtWidgets.QWidget();prog = DAQ_Move(Form1,title="test1",preset=[dict(object='Stage_type_combo',method='setCurrentText',value='PI')],init=False);Form1.show()
    sys.exit(app.exec_())
