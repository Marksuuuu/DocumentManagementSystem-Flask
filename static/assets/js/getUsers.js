$(document).ready(function () {
    getDataFromGetUsers();

    function getDataFromGetUsers() {
        var table = $('#userDataIdTbl').DataTable({
            processing: true,
            ajax: '/getUsers',
            lengthMenu: [[5, 10, 25, 50, -1], [5, 10, 25, 50, "All"]],
            columns: [
                { data: 'id' },
                {
                    data: 'user_pfp',
                    render: function (data) {
                        return '<img src="' + data + '" alt="Profile Picture" width="50" height="50">';
                    }
                },
                { data: 'username' },
                { data: 'firstname' },
                { data: 'lastname' },
                {
                    data: 'user_role',
                    render: function (data) {
                        if (data == 0) {
                            return '<span class="badge bg-success">USER</span>';
                        } else {
                            return '<span class="badge bg-danger">ADMIN</span>';
                        }
                    }
                },
                { data: 'email' }
            ],
            "order": [[1, 'desc']]
        });
    }
});
