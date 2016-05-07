class ProfilesController < ApplicationController
  def edit
    @profile = current_user.profile
    render :edit
  end

  def update
    @profile = Profile.find_by_user_id(params['user_id'])
    @profile.update(profile_params)
    render :edit
  end

  private
  def profile_params
    params.require(:profile).permit(
        :send_to_email
    )
  end
end
