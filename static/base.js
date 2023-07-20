/**------------------------------------------------------------------------
 *                           Document Objects
 *------------------------------------------------------------------------**/

navLogin = document.getElementById("nav_login")
dialogLogin = document.getElementById("dialogLogin")
joinButton = document.getElementById("join_button")


/**------------------------------------------------------------------------
 *                           Login and Signup Dialog
 *------------------------------------------------------------------------**/

/**----------------------
 *    Open Dialogs
 *------------------------**/

navLogin.addEventListener("click", () => {
    dialogLogin.showModal();
})

joinButton.addEventListener("click", () => {
    dialogSignup.showModal();
})


/**----------------------
 *    Close Dialogs
 *------------------------**/

const lightDismiss = ({target:dialog}) => {
    if (dialog.nodeName === 'DIALOG')
      dialog.close('dismiss')
}
document.addEventListener('click', lightDismiss);

/**----------------------
 *    Cloudinary Attempt
 *------------------------**/



