#!/usr/bin/env python3
"""
🪜 scopemate CLI - Command-line interface for scopemate

Provides command-line interface for scopemate with options for setting purpose,
outcome, and output file.
"""

import sys
import argparse
import uuid
from typing import List

from .models import (
    ScopeMateTask, Purpose, Scope, Outcome, Meta, get_utc_now
)
from .storage import save_plan
from .llm import estimate_scope, generate_title_from_purpose_outcome
from .breakdown import suggest_breakdown
from .task_analysis import check_and_update_parent_estimates
from .engine import TaskEngine


def create_task_from_args(purpose: str, outcome: str) -> ScopeMateTask:
    """
    Create a ScopeMateTask from command line arguments.
    
    Args:
        purpose: The purpose description from arguments
        outcome: The outcome description from arguments
        
    Returns:
        A ScopeMateTask object with values from arguments
    """
    # Create a basic task from the command line arguments
    task_id = f"TASK-{uuid.uuid4().hex[:8]}"
    now = get_utc_now()
    
    # Generate a concise title from purpose and outcome
    title = generate_title_from_purpose_outcome(purpose, outcome)
    
    # Create task with basic details
    task = ScopeMateTask(
        id=task_id,
        title=title, 
        purpose=Purpose(
            detailed_description=purpose,
            alignment=[],
            urgency="strategic"
        ),
        scope=Scope(
            size="uncertain",
            time_estimate="sprint",
            dependencies=[],
            risks=[]
        ),
        outcome=Outcome(
            type="customer-facing",
            detailed_outcome_definition=outcome,
            acceptance_criteria=[],
            metric=None,
            validation_method=None
        ),
        meta=Meta(
            status="backlog",
            priority=None,
            created=now,
            updated=now,
            due_date=None,
            confidence="medium"
        ),
        parent_id=None
    )
    
    # Use LLM to estimate scope
    task.scope = estimate_scope(task)
    
    return task


def process_task_with_breakdown(task: ScopeMateTask) -> List[ScopeMateTask]:
    """
    Process a task by generating subtasks and checking estimates.
    
    Args:
        task: The ScopeMateTask to process
        
    Returns:
        List of ScopeMateTask objects including the parent and any subtasks
    """
    # Generate subtasks
    subtasks = suggest_breakdown(task)
    
    # Add all tasks to a list
    all_tasks = [task] + subtasks
    
    # Check and fix estimates
    all_tasks = check_and_update_parent_estimates(all_tasks)
    
    return all_tasks


def command_line() -> None:
    """Process command line arguments and execute appropriate actions."""
    parser = argparse.ArgumentParser(
        description="🪜  scopemate v.0.1.0 - Break down complex projects with LLMs",
        epilog="Purpose: why it matters\n"
               "Outcome: what will change once it's done\n"
               "Scope: how will be delivered (this is where LLM can help)",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Launch guided workflow to define task, generate LLM-powered breakdowns, and estimate scope"
    )
    
    parser.add_argument(
        "--outcome", 
        help="🎯 Outcome: Clearly define what will be delivered and how success will be measured (asks: What will change once this is done?)"
    )

    parser.add_argument(
        "--purpose", 
        help="🧭 Purpose: Clearly define why this project matters strategically (asks: Why does this matter now?)"
    )
    
    parser.add_argument(
        "--output", 
        default="scopemate_plan.json",
        help="JSON file to save the task breakdown and scope estimates (default: scopemate_plan.json)"
    )
    args = parser.parse_args()
    
    # Check if running in interactive mode
    if args.interactive:
        # Run interactive builder
        engine = TaskEngine()
        engine.run()
        return
    
    # Process command-line arguments for non-interactive mode
    if not args.purpose or not args.outcome:
        parser.print_help()
        print("\nError: Both --purpose and --outcome are required in non-interactive mode.")
        sys.exit(1)
    
    # Create task from arguments
    print("Creating task from command line arguments...")
    task = create_task_from_args(args.purpose, args.outcome)
    
    # Process task with subtasks
    print("Generating subtasks...")
    all_tasks = process_task_with_breakdown(task)
    
    # Save plan to output file
    save_plan(all_tasks, args.output)


def main():
    """Main entry point for the scopemate command-line tool."""
    try:
        command_line()
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main() 