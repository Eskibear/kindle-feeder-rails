class SchedulesController < ApplicationController
  def index
    @schedules = Schedule.where(user_id: current_user)
    render :index
  end

  def show
  end

end
