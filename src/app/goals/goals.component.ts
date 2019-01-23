import { Component, OnInit, SimpleChange, OnDestroy } from '@angular/core';
import { AddRemoveGoals } from './add-remove-goals';
import { TaskManager } from '../to-do/add-remove-task';
import { DBAPI } from '../DBAPI.service';
import { Goal } from './goal';
import { from, Subscription } from 'rxjs';
import { Task } from '../to-do/task';
import { MatIconModule } from '@angular/material';
@Component({
  selector: 'app-goals',
  templateUrl: './goals.component.html',
  styleUrls: ['./goals.component.css']
})
export class GoalsComponent implements OnInit, OnDestroy {

  goalsManager: AddRemoveGoals;
  goalsSubscription: Subscription;
  TodayDate: string;
  TM: TaskManager;
  ngOnDestroy(): void {
    this.goalsSubscription.unsubscribe();
  }
  ngOnInit(): void {

  }
  // tslint:disable-next-line:max-line-length
  btnAnimation(btn) {
    btn = btn._elementRef.nativeElement;
    if (btn.classList.contains('ShowStepBtn')) {
      btn.classList.remove('ShowStepBtn');
      btn.classList.add('HideStepBtn');
    }
    else {
      btn.classList.add('ShowStepBtn');
      btn.classList.remove('HideStepBtn');
    }
  }
  // tslint:disable-next-line:max-line-length
  ResetInputStep(title: HTMLInputElement, date: HTMLInputElement, description: HTMLInputElement, addTaskForm: any, thisButton: any) {

    title.value = '';
    date.value = this.TodayDate;
    description.value = '';

  }

  stepsManagerInit(goal: Goal) {
    if (goal.stepsManager === undefined) {
      goal.stepsManager = new TaskManager(this.connectionAPI);
      goal.stepsManager.GetTasks(goal.id);
    }
  }
  // tslint:disable-next-line:max-line-length
  AddGoalButtonClick(title: HTMLInputElement) {
    this.goalsManager.AddGoal(title.value);
    this.ResetInputGoal(title);

  }
  // tslint:disable-next-line:max-line-length
  ResetInputGoal(title: HTMLInputElement) {
    title.value = '';

  }
  AddTaskButtonClick(goal: Goal, title: HTMLInputElement, date: HTMLInputElement, addTaskForm: any): void {
    goal.stepsManager.Add(title.value, new Date(date.value), goal.id);
    this.ResetInput(title, date, addTaskForm);
  }
  ResetInput(title: HTMLInputElement, date: HTMLInputElement, addTaskForm: any): void {
    addTaskForm.style.display = 'none';
    title.value = '';
    date.value = this.TodayDate;
  }
  RemoveGoal(goal: Goal) {
    this.goalsManager.RemoveGoal(goal);
  }
  HideShowElement(el: any): void {
    const display = window.getComputedStyle(el).getPropertyValue('display');
    if (display !== 'none') { el.style.display = 'none'; } else { el.style.display = 'block'; }
  }
  // tslint:disable-next-line:use-life-cycle-interface
  ngDoCheck() {
  }

  DateToStringYYYYMMDD(date: Date): string {
    return date.toISOString().substring(0, 10);
  }
  constructor(private connectionAPI: DBAPI) {
    this.TodayDate = this.DateToStringYYYYMMDD(new Date());
    this.goalsManager = new AddRemoveGoals(this.connectionAPI);
    this.TM = new TaskManager(connectionAPI);
  }



}
